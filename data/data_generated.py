# Use this file to generate different csv file to analyze

import csv
import pickle
import numpy as np
import pandas as pd

fieldnames = ["PT625_1",
              "PT621_1",
              "PT620_1",
              "PT616_1",
              "PT612_1",
              "TE607_1",
              "TE604_1",
              "TE603_1",
              "PT625_2",
              "PT621_2",
              "PT620_2",
              "PT616_2",
              "PT612_2",
              "TE607_2",
              "TE604_2",
              "TE603_2",
              "ITS1", "ITS2", "ITS3", "ITS4", "ITS5"]

# creating a csv-file
with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# Loading all pre-trained models to use:
model = pickle.load(open('../model/MultiOutput_Regressor_DTree', 'rb'))

# Loading the data from Industrial partner:
data_load = 'Oil_lub_system_datafile.csv'
df = pd.read_csv(data_load, sep=',', encoding='utf-8')

# Initial conditions
print('Choose the start-end points and step in the file: ')
int1 = int(input())
int2 = int(input())
step = int(input())

print('Start interval at: ', int1, 'End interval at: ', int2, 'Step size is', step)

count = 0
for i in df.index[int1:int2:step]:
    a = abs(-0.0034 * count ** 4 + 0.0392 * count ** 3 - 0.169 * count ** 2 + 0.299 * count + 0.8306)
    # Use data for stable regimes (velocity > 10 000):
    if df.at[i, 'A_U01_A_ST003_RH1_PV_'] >= 10000:
        pt625_1 = df.at[i, 'A_U01_A_PT625_PR_PV_']
        pt625_2 = df.at[i, 'A_U01_A_PT625_PR_PV_'] * (1 + 0.000000001 * a)
        pt625 = pt625_2 - pt625_1

        pt621_1 = df.at[i, 'A_U01_A_PT621_PR_PV_']
        pt621_2 = df.at[i, 'A_U01_A_PT621_PR_PV_'] * (1 + 0.00000000001 * a)
        pt621 = pt621_2 - pt621_1

        pt620_1 = df.at[i, 'A_U01_A_PT620_PR_PV_']
        pt620_2 = df.at[i, 'A_U01_A_PT620_PR_PV_'] * (1 + 0.00000000001 * a)
        pt620 = pt620_2 - pt620_1

        pt616_1 = df.at[i, 'A_U01_A_PT616_PR_PV_']
        pt616_2 = df.at[i, 'A_U01_A_PT616_PR_PV_'] * (1 - 0.00000000001 * a)
        pt616 = pt616_1 - pt616_2

        pt612_1 = df.at[i, 'A_U01_A_PT612_PR_PV_']
        pt612_2 = df.at[i, 'A_U01_A_PT612_PR_PV_'] * (1 - 0.000000001 * a)
        pt612 = pt612_1 - pt612_2

        te607_1 = df.at[i, 'A_U01_A_TE607_TE_PV_']
        te607_2 = df.at[i, 'A_U01_A_TE607_TE_PV_'] * (1 + 0.000000001 * a)
        te607 = te607_2 - te607_1

        te604_1 = df.at[i, 'A_U01_A_TE604_TE_PV_']
        te604_2 = df.at[i, 'A_U01_A_TE604_TE_PV_'] * (1 + 0.000000001 * a)
        te604 = te604_2 - te604_1

        te603_1 = df.at[i, 'A_U01_A_TE603_TE_PV_']
        te603_2 = df.at[i, 'A_U01_A_TE603_TE_PV_'] * (1 + 0.000000001 * a)
        te603 = te603_2 - te603_1

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
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {"PT625_1": pt625_1,
                    "PT621_1": pt621_1,
                    "PT620_1": pt620_1,
                    "PT616_1": pt616_1,
                    "PT612_1": pt612_1,
                    "TE607_1": te607_1,
                    "TE604_1": te604_1,
                    "TE603_1": te603_1,
                    "PT625_2": pt625_2,
                    "PT621_2": pt621_2,
                    "PT620_2": pt620_2,
                    "PT616_2": pt616_2,
                    "PT612_2": pt612_2,
                    "TE607_2": te607_2,
                    "TE604_2": te604_2,
                    "TE603_2": te603_2,
                    "ITS1": its1,
                    "ITS2": its2,
                    "ITS3": its3,
                    "ITS4": its4,
                    "ITS5": its5
                    }

            csv_writer.writerow(info)
        count += 1
        i += 1
        print(info)
