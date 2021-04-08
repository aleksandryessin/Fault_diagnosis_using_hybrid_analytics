# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

import csv
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

plt.style.use('seaborn-whitegrid')

fieldnames = ["PT625_begin",
              "PT621_begin",
              "PT620_begin",
              "PT616_begin",
              "PT612_begin",
              "TE607_begin",
              "TE604_begin",
              "TE603_begin",
              "PT625_end",
              "PT621_end",
              "PT620_end",
              "PT616_end",
              "PT612_end",
              "TE607_end",
              "TE604_end",
              "TE603_end",
              "ITS1", "ITS2", "ITS3", "ITS4", "ITS5"]

# creating a csv-file
with open('Data/data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Loading all pre-trained models to use:
model = pickle.load(open('model/MultiOutput_Regressor_DTree', 'rb'))

# Loading the data from Industrial partner:
data_load = 'data/Oil_lub_system_datafile.csv'
df = pd.read_csv(data_load, sep=',', encoding='utf-8')

# Initial conditions
print('Choose the start-end points and step in the file: ')
int1 = int(input())
int2 = int(input())
step = int(input())

print('Start interval at: ', int1, 'End interval at: ', int2, 'Step size is', step)


def gen_data(inp1, inp2, s, dataframe, column_name, column_velocity):
    count = 0
    for i in dataframe.index[inp1:inp2:s]:
        # Use data for stable regimes (velocity > 10 000):
        if dataframe.at[i, column_velocity] >= 10000:  # 'A_U01_A_ST003_RH1_PV_'
            begin = df.at[i, column_name]
            end = (1 - 0.005 * count) * df.at[i, column_name]
            diff = begin - end
            count+=1
            i+=1
            return begin, end, diff


for i in df.index[int1, int2, step]:
    pt612 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT612_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[1]
    print(pt612)
'''
def get_its():
    pt625 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT625_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]
    pt621 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT621_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]
    pt620 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT620_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]
    pt616 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT616_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]
    pt612 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_PT612_PR_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]

    te607 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_TE607_TE_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]

    te604 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_TE604_TE_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]

    te603 = gen_data(inp1=int1, inp2=int2, s=step, dataframe=df,
                     column_name='A_U01_A_TE603_TE_PV_',
                     column_velocity='A_U01_A_ST003_RH1_PV_')[2]
    # Preparing X as an input to the model for predicting ITS-values:
    array = (np.array([[pt612], [pt625],
                       [pt616], [pt621],
                       [pt620], [te603],
                       [te604], [te607]]))
    x = array.T

    # Making predictions:
    its1 = round(model.predict(x)[0][0], 2)
    its2 = round(model.predict(x)[0][1], 2)
    its3 = round(model.predict(x)[0][2], 2)
    its4 = round(model.predict(x)[0][3], 2)
    its5 = round(model.predict(x)[0][4], 2)
    # Calculating overall ITS according to the document
    # its = (its1 * its2 * its3 * its4 + its5) / 2

    # Write data to CSV-file for future analysis:
    with open('Data/data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {"PT625": pt625,
                "PT621": pt621,
                "PT620": pt620,
                "PT616": pt616,
                "PT612": pt612,
                "TE607": te607,
                "TE604": te604,
                "TE603": te603,
                "ITS1": get_its()[0],
                "ITS2": get_its()[1],
                "ITS3": get_its()[2],
                "ITS4": get_its()[3],
                "ITS5": get_its()[4]
                }

        csv_writer.writerow(info)

    return its1, its2, its3, its4, its5


def animation1(i):

    j = df.index
    y1 = 
    plt.cla()
    plt.plot(j, y1, label='Normal state sensor')
    plt.plot(j, y2, label='State sensor with malfunction ', linestyle='--')

    plt.legend(loc='upper left')

    plt.title('Current state of the system`s sensors')
    plt.xlabel('Real-Time')
    plt.ylabel('The value of sensor differences or Parameter')

# Animate all your outputs
ani1 = FuncAnimation(plt.gcf(), animation1, interval=1000)
plt.show()
'''