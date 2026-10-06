from mockpatient import MockPatient
import time
import matplotlib.pyplot as plt

patient = MockPatient()

time.sleep(3)

t, v, bp = patient.get_data()

print("Time is {}".format(type(t)))
print(t)

print("Voltage is {}".format(type(v)))
print(v)

plt.plot(t, v)
plt.show()
