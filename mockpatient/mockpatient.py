import numpy as np
from numpy import ndarray
from .ecgsyn import ecgsyn
import time


class MockPatient:

    def __init__(self):
        """
        First, a call to ecgsyn gets an ECG trace for a certain amount of time.
        Since ecgsyn starts the data at the top of an R peak, and we want the
        data obtained from ecgsyn to be repeatable, the third from last R peak
        is found and used as the "end point".

        Based on the time step used by ecgsyn, the time values are calculated
        in the self._time property.  Then the clock time to indicate the start
        time of the patient is saved in the self._start_time_ns property.

        """
        voltage, peaks = ecgsyn(N=128)
        # have the last data point be the third from last peak with label 3
        indices = np.where(peaks == 3)[0]
        t_indices = np.where(peaks == 5)[0]
        last_idx = indices[-3]
        self._voltage = voltage[:last_idx]
        r_peak_indices = indices[indices < last_idx]
        t_peak_indices = t_indices[t_indices < last_idx]

        # Default dt from ecgsyn.  May need to change if different parameter
        #   sent to ecgsyn
        self._dt = 1/256

        self._dt_ns = self._dt * 1e9
        self._final_time = len(self._voltage) * self._dt
        self._final_time_ns = round(self._final_time * 1e9)
        self._time = np.arange(0, self._final_time, self._dt)

        # Build a synthetic arterial blood pressure waveform synchronized
        # to the ECG cycle timing.
        self._bp = self._generate_bp_waveform(len(self._voltage),
                                              r_peak_indices,
                                              t_peak_indices,
                                              self._dt)

        self._start_time_ns = time.monotonic_ns()
        self._last_acq_time_ns = self._start_time_ns

    @staticmethod
    def _generate_bp_waveform(
                              n_samples: int,
                              r_peak_indices: np.ndarray,
                              t_peak_indices: np.ndarray,
                              dt: float,
                              sbp: float = 120.0,
                              dbp: float = 80.0,
                              r_to_upstroke_delay_s: float = 0.18,
                              rise_time_s: float = 0.08,
                              decay_tau_s: float = 0.25,
                              ) -> np.ndarray:
        """
        Generate a synthetic arterial blood pressure waveform aligned to actual
        R-peak locations in the ECG data.

        For each beat, the pressure pulse begins r_to_upstroke_delay_s after
        the R-peak, rises over rise_time_s using a smoothstep, then decays
        exponentially toward DBP for the remainder of the beat.  Added a normal
        distribution centered around the delayed T peak to simulate the
        dicrotic notch.

        Args:
            n_samples (int): Total number of samples in the ECG array.
            r_peak_indices (ndarray): Sample indices of R peaks.
            t_peak_indices (ndarray): Sample indices of T peaks.
            dt (float): Sample period in seconds.
            sbp (float): Systolic blood pressure (mmHg).
            dbp (float): Diastolic blood pressure (mmHg).
            r_to_upstroke_delay_s (float): Delay from R peak to pressure
                                            upstroke.
            rise_time_s (float): Duration of pressure rise.
            decay_tau_s (float): Exponential decay time constant.  No longer
                used in current implementation that forces decline to go back
                to dbp.

        Returns:
            ndarray: Blood pressure samples (mmHg), same length as ECG array.
        """
        bp = np.full(n_samples, dbp, dtype=float)
        delay_samples = round(r_to_upstroke_delay_s / dt)
        rise_samples = round(rise_time_s / dt)

        # Determine beat boundaries: upstroke start to next upstroke start
        upstroke_starts = r_peak_indices + delay_samples
        dicratic_starts = t_peak_indices + delay_samples

        for i, start in enumerate(upstroke_starts):
            # Beat runs from this upstroke to the next (or end of array)
            if i + 1 < len(upstroke_starts):
                beat_end = upstroke_starts[i + 1]
            else:
                beat_end = n_samples
            diacratic_start = dicratic_starts[i]
            if diacratic_start >= n_samples:
                diacratic_start = -1
            if start >= n_samples:
                break

            beat_end = min(beat_end, n_samples)
            beat_len = beat_end - start

            # Rising portion
            rise_end = min(start + rise_samples, beat_end)
            n_rise = rise_end - start
            if n_rise > 0:
                x = np.linspace(0.0, 1.0, n_rise, endpoint=False)
                bp[start:rise_end] = dbp + (sbp - dbp) * (3 * x**2 - 2 * x**3)

            # Decaying portion
            k = np.log((sbp-dbp) / 0.1) / ((beat_end - rise_end) * dt)
            decay_tau_s = 1 / k
            beta = 1.3
            notch_mean = (diacratic_start - start) * dt
            notch_sd = 0.02
            notch_amplitude = (sbp - dbp) * 0.006
            notch_prefix = 1/(notch_sd * np.sqrt(2 * np.pi))
            if rise_end < beat_end:
                td = np.arange(0, beat_end - rise_end) * dt
                bp[rise_end:beat_end] = (dbp
                                         + (sbp - dbp) * np.exp(-td**beta /
                                                                decay_tau_s)
                                         + notch_amplitude * notch_prefix
                                         * np.exp(-0.5 * ((td - notch_mean) /
                                                          notch_sd)**2))

        return bp

    def _convert_ns_to_cycles_index(self, time_ns: int) -> tuple[int, int]:
        """
        Determines the index and the number of cycles from the ecg data that
        corresponds to the given input time.

        The ECG data consists of a discrete data set of voltages versus time.
        When the program run time exceeds the length of this time, the ecg data
        is repeated in a loop.  When a request for data is made at a certain
        program time, it is necessary to determine where that program time is
        in the ecg data.  This function calculates how many times has the ecg
        data cycled and what index of the ecg data corresponds to the current
        program time.

        First, the total elapsed program time is determined.  The number of
        previous cycles is calculated and then the index matching the current
        time is determined.

        Args:
            time_ns (int): Clock time in nanoseconds.

        Returns:
            int: number of previous ecg data cycles
            int: index of the current ecg data cycle

        """
        delta_ns = time_ns - self._start_time_ns
        cycles = delta_ns // self._final_time_ns
        time_into_ns = delta_ns % self._final_time_ns
        index = round(time_into_ns / self._dt_ns)
        return cycles, index

    def get_data(self) -> tuple[ndarray, ndarray, ndarray]:
        """Returns ECG and BP data available since last inquiry

        The current clock time is converted into a number of cycles and the
        current index based on the current program run time.  The number of
        cycles and index at the last data acquisition is determined.  Using the
        before and current time, the needed data is obtained from the ECG data
        and returned.

        Returns:
            ndarray: program time of samples
            ndarray: ECG voltage samples
            ndarray: Blood pressure samples (mmHg)
        """
        # ToDo:  Double check correctness of data if start_cycle != end_cycle
        current_time_ns = time.monotonic_ns()
        end_cycle, end_index = self._convert_ns_to_cycles_index(
            current_time_ns)
        start_cycle, start_index = self._convert_ns_to_cycles_index(
            self._last_acq_time_ns
        )

        if start_cycle == end_cycle:
            ecg = self._voltage[start_index:end_index]
            bp = self._bp[start_index:end_index]
            prog_time = (
                self._time[start_index:end_index]
                + end_cycle * self._final_time
            )
        else:
            ecg = self._voltage[start_index:]
            bp = self._bp[start_index:]
            prog_time = (self._time[start_index:]
                         + start_cycle * self._final_time)

            for i in range(end_cycle - start_cycle - 1):
                ecg = np.append(ecg, self._voltage)
                bp = np.append(bp, self._bp)
                prog_time = np.append(
                    prog_time,
                    self._time + (start_cycle + i + 1) * self._final_time
                )

            ecg = np.append(ecg, self._voltage[:end_index])
            bp = np.append(bp, self._bp[:end_index])

            # NOTE: [:end_index] matches data slice;
            #           avoids length mismatch bug.
            prog_time = np.append(
                prog_time,
                self._time[:end_index] + end_cycle * self._final_time
            )

        self._last_acq_time_ns = current_time_ns
        return prog_time, ecg, bp
