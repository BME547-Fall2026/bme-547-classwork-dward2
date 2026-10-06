import math
from typing import Union
import numpy as np
from scipy.signal import resample_poly
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def ecgsyn(*,
           sfecg: int = 256,
           N: int = 256,
           Anoise: float = 0.0,
           hrmean: float = 60.0,
           hrstd: float = 1.0,
           lfhfratio: float = 0.5,
           sfint: int = 512,
           ti: Union[list[float], None] = None,
           ai: Union[list[float], None] = None,
           bi: Union[list[float], None] = None):
    """
    Produces synthetic ECG

    Args:
        sfecg: ECG sampling frequency [256 Hertz default]
        N: approximate number of heart beats [256 default]
        Anoise: Additive uniformly distributed measurement noise [0 mV default]
        hrmean: Mean heart rate [60 bpm default]
        hrstd: Standard deviation of heart rate [1 bpm default]
        lfhfractio: LF/HF ratio [0.5 default]
        sfint: Internal sampling frequency [512 Hertz default]
        ti: angles (degrees) of extrema for [P Q R S T] [-70 -15 0 15 100 default]
        ai: z-position of extrema for [P Q R S T] [1.2 -5 30 -7.5 0.75 default]
        bi: Gaussian width of peaks for [P Q R S T] [0.25 0.1 0.1 0.1 0.4 default]

    Returns:
        s: ECG (mv)
        ipeaks: labels for PQRST peaks: P(1), Q(2), R(3), S(4), T(5)


    """
    if ti is None:
        ti = [-70, -15, 0, 15, 100]
    if ai is None:
        ai = [1.2, -5.0, 30.0, -7.5, 0.75]
    if bi is None:
        bi = [0.25, 0.1, 0.1, 0.1, 0.4]

    # convert lists to ndarrays
    ti = np.array(ti)
    ai = np.array(ai)
    bi = np.array(bi)

    # Convert ti from degrees to radians
    ti = ti * np.pi / 180

    # Adjust extrema parameters for mean heart rate
    hrfact = math.sqrt(hrmean / 60)
    hrfact2 = math.sqrt(hrfact)
    bi = hrfact * bi
    ti = np.array([hrfact2, hrfact, 1, hrfact, hrfact2]) * ti

    # Check that sfint is an integer multiple of sfecg
    q = round(sfint/sfecg)
    qd = sfint/sfecg
    if q != qd:
        raise ValueError('Internal sampling frequency {} must be an integer '
                         'multiple of the ECG sampling frequency {}.'
                         .format(sfint, sfecg))

    # Define frequency parameters for rr process
    # flo and fhi correspond to the Mayer waves and respiratory rate
    flo = 0.1
    fhi = 0.25
    flostd = 0.01
    fhistd = 0.01

    # Calculate time scales for rr and total output
    sampfreqrr = 1
    trr = 1 / sampfreqrr
    tstep = 1 / sfecg
    rrmean = (60 / hrmean)
    Nrr = 2**(math.ceil(np.log2(N*rrmean/trr)))
    
    # Compute rr process
    rr0 = rrprocess(flo, fhi, flostd, fhistd, lfhfratio, hrmean, hrstd,
                    sampfreqrr, Nrr)

    # upsample rr time series from 1 Hz to sfint Hz
    rr = resample_poly(rr0, sfint, 1)

    # make the rrn time series
    dt = 1/sfint
    rrn = np.zeros(len(rr))
    tecg = 0
    i = 0
    while i <= len(rr)-1:
        tecg = tecg+rr[i]
        ip = round(tecg/dt)
        rrn[i:ip] = rr[i]
        i = ip
    Nt = ip

    # integrate system using fourth order Runge-Kutta
    # print("Integrating dynamical system")
    x0 = [1.0, 0.0, 0.04]
    Tspan = np.arange(0, math.floor(Nt * dt), dt)
    sol = solve_ivp(
        lambda t, x: derivsecgsyn(t, x, rrn, sfint, ti, ai, bi),
        (Tspan[0], Tspan[-1]),
        x0,
        t_eval=Tspan,
        method='RK45'
    )
    T = sol.t
    X0 = sol.y.T

    # downsample to required sfecg
    X = X0[::q, :]

    # extract R-peaks times
    ipeaks = detectpeaks(X, ti, sfecg)

    # Scale signal to lie between -0.4 and 1.2 mV
    z = X[:, 2]
    zmin = np.min(z)
    zmax = np.max(z)
    zrange = zmax - zmin
    z = (z - zmin) * 1.6 / zrange - 0.4

    # include additive uniformly distributed measurement noise
    eta = 2 * np.random.rand(len(z)) - 1
    s = z + Anoise * eta

    return s, ipeaks


def rrprocess(flo, fhi, flostd, fhistd, lfhfratio, hrmean, hrstd, sfrr, n):
    w1 = 2 * np.pi * flo
    w2 = 2 * np.pi * fhi
    c1 = 2 * np.pi * flostd
    c2 = 2 * np.pi * fhistd
    sig2 = 1
    sig1 = lfhfratio
    rrmean = 60 / hrmean
    rrstd = 60 * hrstd / (hrmean * hrmean)

    df = sfrr / n
    w = np.arange(n) * 2 * np.pi * df
    dw1 = w - w1
    dw2 = w - w2

    Hw1 = sig1 * np.exp(-0.5 * (dw1 / c1) ** 2) / np.sqrt(2 * np.pi * c1 ** 2)
    Hw2 = sig2 * np.exp(-0.5 * (dw2 / c2) ** 2) / np.sqrt(2 * np.pi * c2 ** 2)
    Hw = Hw1 + Hw2
    Hw0 = np.concatenate((Hw[:n // 2], Hw[n // 2 - 1::-1]))
    Sw = (sfrr / 2) * np.sqrt(Hw0)

    ph0 = 2 * np.pi * np.random.rand(round(n / 2 - 1))

    ph = np.concatenate([[0], ph0, [0], -np.flipud(ph0)])
    SwC = Sw * np.exp(1j * ph)
    x = (1 / n) * np.real(np.fft.ifft(SwC))

    xstd = np.std(x, ddof=1)
    ratio = rrstd / xstd
    rr = rrmean + x * ratio
    return rr


def derivsecgsyn(t, x, rr, sfint, ti, ai, bi):
    xi = np.cos(ti)
    yi = np.sin(ti)
    ta = np.atan2(x[1], x[0])
    r0 = 1
    a0 = 1.0 - np.sqrt(x[0] ** 2 + x[1] ** 2) / r0
    ip = int(np.floor(t * sfint))
    w0 = 2 * np.pi / rr[ip]

    fresp = 0.25
    zbase = 0.005 * np.sin(2 * np.pi * fresp * t)

    dx1dt = a0 * x[0] - w0 * x[1]
    dx2dt = a0 * x[1] + w0 * x[0]

    dti = np.fmod(ta - ti, 2 * np.pi)
    dx3dt = - np.sum(ai * dti * np.exp(-0.5 * (dti / bi) ** 2)) - 1.0 * (
                x[2] - zbase)

    dxdt = np.array([dx1dt, dx2dt, dx3dt])
    return dxdt


def detectpeaks(X, thetap, sfecg):
    N = len(X)
    irpeaks = np.zeros(N)

    theta = np.atan2(X[:, 1], X[:, 0])
    ind0 = np.zeros(N)
    for i in range(N-1):
        a = ((theta[i] <= thetap) & (thetap <= theta[i+1]))
        j = np.where(a == 1)[0]
        if len(j) != 0:
            d1 = thetap[j[0]] - theta[i]
            d2 = theta[i+1] - thetap[j[0]]
            if d1 < d2:
                ind0[i] = j[0] + 1
            else:
                ind0[i+1] = j[0] + 1

    d = math.ceil(sfecg/64)
    d = max(2, d)
    ind = np.zeros(N)
    z = X[:, 2]
    zmin = min(z)
    zmax = max(z)
    zext = np.array([zmin, zmax, zmin, zmax, zmin])
    sext = np.array([1, -1, 1, -1, 1])
    for i in range(1, 6):
        ind1 = np.where(ind0 == i)[0]
        n = len(ind1)
        Z = np.ones((n, 2*d+1))*zext[i-1]*sext[i-1]
        for j in range(-d, d):
            k = np.where((0 <= ind1+j) & (ind1+j <= N-1))[0]
            Z[k, d+j+1] = z[ind1[k]+j] * sext[i-1]
        vmax = np.max(Z, axis=1)
        ivmax = np.argmax(Z, axis=1)
        iext = ind1 + ivmax - d - 1
        ind[iext] = i
    return ind


def identify(a, b):
    x = []
    y = []
    for i in range(len(a)):
        if b[i] != 0:
            x.append(i)
            y.append(a[i])
    return x, y


if __name__ == '__main__':
    a, b = ecgsyn()
    x, y = identify(a, b)
    plt.plot(a)
    plt.plot(x, y, "ro")
    plt.show()
