import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('robot.txt', sep=' ', header=None)
data = data.drop([1, 3], axis=1)
data.columns = ["TimeStamp", "Power"]
data.TimeStamp = pd.to_datetime(data.TimeStamp)
data['time'] = (data.TimeStamp - data.TimeStamp[0]).dt.total_seconds()
data = data.groupby('TimeStamp').mean().reset_index()
data['5s SMA'] = data.rolling(10).mean().iloc[:, 0]
data['5s SMA'] = np.log10(data['5s SMA'])
data['fft'] = np.fft.fft(data['5s SMA'])
data['CMA'] = data.Power.expanding().mean()
print(data.fft)

'''fig = plt.figure()
plt.rcParams.update({'text.color': "red",'axes.labelcolor': "red",'xtick.color':"red",'ytick.color':"red"})
fig.patch.set_facecolor([0.1373,0.1529,0.2392])
ax = fig.add_subplot(312)
ax.set_facecolor([0.1373,0.1529,0.2392])
ax.plot(data.time,data['5s SMA'],'r-',linewidth= 0.4)
ax.axis([data['time'].min(), data['time'].max(), 0,data['5s SMA'].mean()+10*data['5s SMA'].std()])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Power (W)')
ax.set_title('Robot Power Consumption (10s Moving Average)')




fig.patch.set_facecolor([0.1373,0.1529,0.2392])
ax1 = fig.add_subplot(313)
ax1.set_facecolor([0.1373,0.1529,0.2392])
ax1.plot(data.time,data['CMA'],'r-',linewidth= 0.6)
ax1.axis([data['time'].min(), data['time'].max(), 0, 1500])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Power (W)')
ax1.set_title('Robot Power Consumption (Cumulative Average)')


plt.rcParams.update({'text.color': "red",'axes.labelcolor': "red",'xtick.color':"red",'ytick.color':"red"})
fig.patch.set_facecolor([0.1373,0.1529,0.2392])
ax = fig.add_subplot(311)
ax.set_facecolor([0.1373,0.1529,0.2392])
ax.plot(data.time,data['fft'],'r-',linewidth= 0.4)
#ax.axis([data['time'].min(), data['time'].max(), 0,data['5s SMA'].mean()+10*data['5s SMA'].std()])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Power (W)')
ax.set_title('Robot Power Consumption (10s Moving Average)')

plt.show()'''
