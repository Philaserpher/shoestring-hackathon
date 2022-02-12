import serial
import numpy as np
import matplotlib.pyplot as plt

RED = [0.9412, 0.3647, 0.3647]
S = serial.Serial("COM7", 115200)
data = []
time_array = []

fig1 = plt.figure()
fig1.patch.set_facecolor([0.1373, 0.1529, 0.2392])
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_facecolor([0.1373, 0.1529, 0.2392])
ax1.plot(time_array, data, color=RED, linewidth=0.6)
# ax1.axis([data.min(), data['time'].max(),
# 0, data['CMA'].mean()+data['CMA'].std()])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Power (W)')
ax1.set_title('Robot Power Consumption (Cumulative Average)')


for i in range(2):
    S.readline()
for i in range(1000):
    print("A")
    time_array.append(i)
    data.append(float((S.readline().decode())))
    ax1.plot(time_array, data, color=RED, linewidth=0.6)
    plt.pause(0.05)
