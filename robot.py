import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('robot.txt', sep=' ', header=None)
data = data.drop([1, 3], axis=1)
data.columns = ["TimeStamp", "Power"]
data.TimeStamp = pd.to_datetime(data.TimeStamp)
data['time'] = (data.TimeStamp - data.TimeStamp[0]).dt.total_seconds()
data = data.groupby('TimeStamp').mean().reset_index()
data['10s_SMA'] = data['Power'].rolling(10).mean()
data['10s_SMA'] = np.log10(data['10s_SMA'])
data['CMA'] = data.Power.expanding().mean()
data['fft'] = data['Power'].interpolate()

for i in range(10):
    data['fft'][i] = 0
data['fft'].apply(lambda x :np.hanning(1))
data['fft'] = np.fft.fft(data['fft'])
data['fft'] = data['fft'].abs()
fvals = np.fft.fftfreq(len(data['fft']), d=1/3600)
fvals = fvals[:len(data.fft)]


fig = plt.figure()

plt.rcParams.update({'text.color': "red", 'axes.labelcolor': "red",
                     'xtick.color': "red", 'ytick.color': "red"})
fig.patch.set_facecolor([0.1373, 0.1529, 0.2392])
ax = fig.add_subplot(312)
ax.set_facecolor([0.1373, 0.1529, 0.2392])
ax.plot(data.time, data['10s_SMA'], 'r-', linewidth=0.4)
ax.axis([data['time'].min(), data['time'].max(), 0,
         data['10s_SMA'].mean()+12*data['10s_SMA'].std()])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Power (W)')
ax.set_title('Robot Power Consumption (10s Moving Average)')


fig.patch.set_facecolor([0.1373, 0.1529, 0.2392])
ax1 = fig.add_subplot(313)
ax1.set_facecolor([0.1373, 0.1529, 0.2392])
ax1.plot(data.time, data['CMA'], 'r-', linewidth=0.6)
ax1.axis([data['time'].min(), data['time'].max(), 0, data['CMA'].mean()+1*data['CMA'].std()])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Power (W)')
ax1.set_title('Robot Power Consumption (Cumulative Average)')


plt.rcParams.update({'text.color': "red", 'axes.labelcolor': "red",
                     'xtick.color': "red", 'ytick.color': "red"})
fig.patch.set_facecolor([0.1373, 0.1529, 0.2392])
ax2 = fig.add_subplot(311)
ax2.set_facecolor([0.1373, 0.1529, 0.2392])
ax2.plot(fvals, data['fft'], 'r-', linewidth=0.4)
ax2.axis([0, 75, 0, 400000])
ax2.set_xlabel('Frequency (1/s)')
ax2.set_ylabel('Power (W)')
ax2.set_title('Robot Power Consumption (10s Moving Average)')
plt.subplots_adjust(hspace=0.5)
plt.show()
