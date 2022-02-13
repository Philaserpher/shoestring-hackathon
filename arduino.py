import serial
import matplotlib.pyplot as plt
import numpy as np

DT = 0.5

RED = [0.9412, 0.3647, 0.3647]
BLUE = [0.1960, 0.3373, 0.6588]
GREEN = [0.1176, 0.6112, 0.2]
BG_COLOUR = [0.1373, 0.1529, 0.2392]

S = serial.Serial("COM7", 115200)  # initialise serial at 115200 baud rate
# create a dataframe
DATA = [np.array([]), np.array([]), np.array([]), np.array([])]
# this will be used to store and process all of our data

# create out figure
fig1 = plt.figure(figsize=(19, 10))
fig1.patch.set_facecolor(BG_COLOUR)

# set up our first plot
AX1 = fig1.add_subplot(2, 2, 1)
AX1.set_facecolor(BG_COLOUR)
AX1.set_xlabel('Time (s)')
AX1.set_ylabel('Power (W)')
AX1.set_title('Fan Power Consumption')
# raw data vs time


def plot_raw(ax1, data):
    g1, = ax1.plot(data[0], data[1], color=RED, linewidth=0.6)
    g2, = ax1.plot(data[0], data[2], color=BLUE, linewidth=0.6)
    leg = ax1.legend([g1, g2], ['Raw Data', '5 Second Average'],
                     loc='lower right', facecolor=BG_COLOUR)
    for text in leg.get_texts():
        text.set_color(RED)


# set up second plot
AX2 = fig1.add_subplot(2, 2, 2)
AX2.set_facecolor(BG_COLOUR)
AX2.set_xlabel('Time (s)')
AX2.set_ylabel('Power (W)')
AX2.set_title('Fan Power Consumption (Cumulative Average)')


def plot_cumulative(ax2, data, max, max_pos, annotation, power_usage,
                    power_usage_total):
    g1, = ax2.plot(data[0], data[3], color=RED, linewidth=0.6)
    g2, = ax2.plot(data[0], data[3]+5, color=BLUE, linewidth=0.6)
    g3, = ax2.plot(data[0], data[3]-5, color=GREEN, linewidth=0.6)
    ax2.legend([g2, g1, g3],
               ['Upper Bound', 'Cumulative Average', 'Lower Bound'],
               loc='lower left', facecolor=BG_COLOUR)
    ax2.axis([data[0].min(), data[0].max(),
              data[3].min()-50, data[3].max()+50])
    if data[3][-1]+5 >= max:
        try:
            annotation.remove()
        except:
            pass
        max = int(data[3][-1]+5)
        max_pos = data[0][-1]
        max_plot = round(max*0.001, 3)
        annotation = ax2.annotate(f"{max_plot} W", (max_pos, max+20), size=14, ha='right',
                                  va='top', bbox=dict(boxstyle='round',
                                                      fc=BG_COLOUR))
    average_rate_hour = int(data[3][-1]*3.6)
    try:
        power_usage.remove()
        power_usage_total.remove()
    except:
        pass
    power_usage = ax2.annotate(f"{average_rate_hour} J/h",
                               xy=(data[0][-1], max-50),
                               size=14, ha='right', va='top',
                               bbox=dict(boxstyle='round', fc=BG_COLOUR))

    total_power_used = round(data[3][-1]*data[0][-1]*0.001, 2)

    power_usage_total = ax2.annotate(f"{total_power_used} J used",
                                     xy=(data[0][-1], max-70),
                                     size=14, ha='right', va='top',
                                     bbox=dict(boxstyle='round', fc=BG_COLOUR))
    return max, max_pos, annotation, power_usage, power_usage_total


AX3 = fig1.add_subplot(2, 2, 3)
AX3.set_facecolor(BG_COLOUR)
AX3.set_xlabel('Time (s)')
AX3.set_ylabel('Power (W)')
AX3.set_title('Fan Power Consumption (Box Plot)')


def plot_box(ax3, data):
    ax3.cla()
    ax3.boxplot(data[1])


counter = 0.0
MAX = 0
MAX_POS = 0
ANNOTATION = 0
POWER_USAGE = 0
POWER_USAGE_TOTAL = 0
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
    MAX, MAX_POS, ANNOTATION, POWER_USAGE, POWER_USAGE_TOTAL = plot_cumulative(
        AX2, DATA, MAX, MAX_POS, ANNOTATION, POWER_USAGE, POWER_USAGE_TOTAL)
    plot_box(AX3, DATA)
    counter += DT
    plt.pause(0.5)



filtered_power = data[2]*np.hanning(len(data[2]))
for i in range(5):
    filtered_power[i] = 0
filtered_power = (np.fft.fft(filtered_power)).abs()
fvals = np.fft.fftfreq(len(filtered_power), d=1/3600)