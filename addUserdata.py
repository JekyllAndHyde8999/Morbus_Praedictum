import pandas as pd

df = pd.read_csv("UserModelGen.csv", header=0, skipinitialspace=True)

list_dicts = []

for _, row in df.iterrows():
    print(dict(row))

