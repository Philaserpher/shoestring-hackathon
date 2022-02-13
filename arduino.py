import serial
import matplotlib.pyplot as plt
import numpy as np

DT = 0.5

RED = [0.9412, 0.3647, 0.3647]
BLUE = [0.1960, 0.3373, 0.6588]
BG_COLOUR = [0.1373, 0.1529, 0.2392]

S = serial.Serial("COM7", 115200)  # initialise serial at 115200 baud rate
# create a dataframe
DATA = [np.array([]), np.array([]), np.array([]), np.array([])]
# this will be used to store and process all of our data

# create out figure
fig1 = plt.figure()
fig1.patch.set_facecolor(BG_COLOUR)

# set up our first plot
AX1 = fig1.add_subplot(1, 2, 1)
AX1.set_facecolor(BG_COLOUR)
AX1.set_xlabel('Time (s)')
AX1.set_ylabel('Power (W)')
AX1.set_title('Fan Power Consumption')
# raw data vs time


def plot_raw(ax1, data):
    print(data[0], data[1])
    ax1.plot(data[0], data[1], color=RED, linewidth=0.6)
    ax1.plot(data[0], data[2], color=BLUE, linewidth=0.6)


# set up second plot
AX2 = fig1.add_subplot(1, 2, 2)
AX2.set_facecolor(BG_COLOUR)
AX2.set_xlabel('Time (s)')
AX2.set_ylabel('Power (W)')
AX2.set_title('Fan Power Consumption (Cumulative Average)')


def plot_cumulative(ax2, data):
    ax2.plot(data[0], data[3], color=RED, linewidth=0.6)
    ax2.axis([data[0].min(), data[0].max(), 0, data[1].max()])


counter = 0.0
while True:
    new_value = float(S.readline().decode())

    if counter >= 5.0:
        points = round(5.0/DT)
        five_second_average = sum(DATA[1][-points:])/points
    else:
        five_second_average = 0

    if len(DATA[1]):
        cumulative_average = sum(DATA[1])/len(DATA[1])
    else:
        cumulative_average = new_value

    DATA[0] = np.append(DATA[0], counter)
    DATA[1] = np.append(DATA[1], new_value)
    DATA[2] = np.append(DATA[2], five_second_average)
    DATA[3] = np.append(DATA[3], cumulative_average)

    plot_raw(AX1, DATA)
    plot_cumulative(AX2, DATA)
    counter += DT
    plt.pause(0.05)
