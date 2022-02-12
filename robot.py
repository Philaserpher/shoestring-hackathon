import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('robot.txt', sep=' ', header=None)
data = data.drop([1, 3], axis=1)
data.columns = ["TimeStamp", "Power"]
data.TimeStamp = pd.to_datetime(data.TimeStamp)
data['time'] = (data.TimeStamp - data.TimeStamp[0]).dt.total_seconds()
data = data.groupby('TimeStamp').mean().reset_index()
<<<<<<< HEAD
data['5s SMA'] = data.rolling(10).mean().iloc[:,0]
=======
data['5s SMA'] = data.rolling(1).mean().iloc[:, 0]
>>>>>>> 20f4d76cb3fb58ff3c2c523faa0dd31ced2ab5a7
data['CMA'] = data.Power.expanding().mean()
# print(data)


'''sns.reset_defaults()
sns.set(rc={'figure.figsize':(7,5)}, style="white")'''
<<<<<<< HEAD
fig = plt.figure()
plt.rcParams.update({'text.color': "red",'axes.labelcolor': "red",'xtick.color':"red",'ytick.color':"red"})
fig.patch.set_facecolor([0.1373,0.1529,0.2392])
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor([0.1373,0.1529,0.2392])
ax.plot(data.time,data['5s SMA'],'r-',linewidth= 0.4)
ax.axis([data['time'].min(), data['time'].max(), 0, data['5s SMA'].mean()+5*data['5s SMA'].std()])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Power (W)')
ax.set_title('Robot Power Consumption (10s Moving Average)')



fig1 = plt.figure()
fig1.patch.set_facecolor([0.1373,0.1529,0.2392])
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_facecolor([0.1373,0.1529,0.2392])
ax1.plot(data.time,data['CMA'],'r-',linewidth= 0.6)
ax1.axis([data['time'].min(), data['time'].max(), 0, data['5s SMA'].mean()+5*data['5s SMA'].std()])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Power (W)')
ax1.set_title('Robot Power Consumption (Cumulative Average)')
plt.show()
=======
plt.plot(data.time, data['5s SMA'], 'r-')
plt.axis([data['time'].min(), data['time'].max(), 0,
          data['5s SMA'].mean()+5*data['5s SMA'].std()])
plt.set_facecolor('xkcd:salmon')
plt.show()
>>>>>>> 20f4d76cb3fb58ff3c2c523faa0dd31ced2ab5a7
