# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# import numpy as np

plt.style.use('seaborn-whitegrid')

# Initial conditions
'''print('Choose the start-end points and step in the file: ')
int1 = int(input())
int2 = int(input())
step = int(input())

print('Start interval at: ', int1, 'End interval at: ', int2, 'Step size is', step)'''

data = pd.read_csv('data/data.csv')
x = []
for j in data.index:
    x.append(j)

fig, ax = plt.subplots(2, 1)

ax1, ax2 = ax.flatten()

# Set axes limits for tags
ax1.set(xlim=(0, 700), ylim=(5, 55))
# Draw a blank line for tags
line1, = ax1.plot([], [], label='Normal state sensor')
line2, = ax1.plot([], [], label='State sensor with malfunction ', linestyle='--')

# Set axes limits for malfunctions
ax2.set(xlim=(0, 700), ylim=(0, 1.1))
# Draw a blank line for malfunctions
line1m, = ax2.plot([], [], label='ITS of the malfunction after main GG pump')
line2m, = ax2.plot([], [], label='ITS of the malfunction after hoses')
line3m, = ax2.plot([], [], label='ITS of the malfunction after ball-valve')
line4m, = ax2.plot([], [], label='ITS of the malfunction after check-valve')
line5m, = ax2.plot([], [], label='ITS of the malfunction before hydraulic system')


# Define data for tags
y1 = data['PT612_1']
y2 = data['PT612_2']

# Define data for malfunctions
y1m = data['ITS1']
y2m = data['ITS2']
y3m = data['ITS3']
y4m = data['ITS4']
y5m = data['ITS5']

# Settings for plots
ax1.legend(loc='lower left')
ax1.set_title('Current state of the systems sensors')
ax1.set_xlabel('Real-Time')
ax1.set_ylabel('The value of sensor differences or Parameter')

ax2.legend(loc='lower left')
ax2.set_title('Current state of the systems malfunctions')
ax2.set_xlabel('Real-Time')
ax2.set_ylabel('The value of the parameters ITS')


# Define animate function
def animate1(i):
    line1.set_data(x[:i], y1[:i])
    line2.set_data(x[:i], y2[:i])
    time.sleep(0.01)
    return line1, line2,


# Define animate function
def animate2(i):
    line1m.set_data(x[:i], y1m[:i])
    line2m.set_data(x[:i], y2m[:i])
    line3m.set_data(x[:i], y3m[:i])
    line4m.set_data(x[:i], y4m[:i])
    line5m.set_data(x[:i], y5m[:i])
    time.sleep(0.01)
    return line1m, line2m, line3m, line4m, line5m,


# Animations
ani1 = FuncAnimation(plt.gcf(), animate1, interval=20)
ani2 = FuncAnimation(plt.gcf(), animate2, interval=20)
plt.tight_layout()
plt.show()
