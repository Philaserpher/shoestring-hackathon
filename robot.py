import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('robot.txt',sep=' ' ,header=None)
data = data.drop([1,3],axis=1)
data.columns = ["TimeStamp", "Power"]
data.TimeStamp = pd.to_datetime(data.TimeStamp)
data['time'] = (data.TimeStamp - data.TimeStamp[0]).dt.total_seconds()
data = data.groupby('TimeStamp').mean().reset_index()
data['5s SMA'] = data.rolling(1).mean().iloc[:,0]
data['CMA'] = data.Power.expanding().mean()
#print(data)


'''sns.reset_defaults()

sns.set(rc={'figure.figsize':(7,5)}, style="white")'''
plt.plot(data.time,data['5s SMA'],'r-')
plt.axis([data['time'].min(), data['time'].max(), 0, data['5s SMA'].mean()+5*data['5s SMA'].std()])
plt.set_facecolor('xkcd:salmon')
plt.show()