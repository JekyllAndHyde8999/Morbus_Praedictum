import pandas as pd
import datetime
import numpy as np

TOP_K = 11

specials = [
    "Physiatrist",
    "Rheumatologist",
    "General Physician",
    "Neurologist",
    "Allergist"
]

qualifs = [
    "MBBS",
    "MS",
    "MD",
    "DCH",
    "BSc"
]


def parseDates(x):
    date_obj = datetime.datetime.strptime(x, "%d/%m/%Y")
    return date_obj.date()


def getEmail(x):
    username = ''.join(x.split()).lower()
    return username + "@gmail.com"


def getGender(x):
    return {'M': 1, 'F': 2}[x]


df = pd.read_csv('fake_data.csv', header=0, skipinitialspace=True)
new_df = pd.DataFrame(columns=["index",
                               "Doctor_First_Name",
                               "Doctor_Last_Name",
                               "Doctor_DOB",
                               "Doctor_Email",
                               "Doctor_Gender",
                               "Doctor_Qualifications",
                               "Doctor_Specialization",
                               "Doctor_Experience",
                               "Doctor_License",
                               "Doctor_Activate"])
new_df = new_df.set_index(["index"])

new_df["Doctor_First_Name"] = df["Name"].apply(lambda x: x.split()[0])
new_df["Doctor_Last_Name"] = df["Name"].apply(lambda x: x.split()[1])
new_df["Doctor_DOB"] = df["DOB"].apply(parseDates)
new_df["Doctor_Email"] = df["Name"].apply(getEmail)
new_df["Doctor_Gender"] = df["Sex"].apply(getGender)
new_df["Doctor_Qualifications"] = [np.random.choice(qualifs) for _ in range(df.shape[0])]
new_df["Doctor_Specialization"] = [np.random.choice(specials) for _ in range(df.shape[0])]
new_df["Doctor_Experience"] = [np.random.randint(1, 15) for _ in range(df.shape[0])]
new_df["Doctor_License"] = df["ID"].apply(lambda x: str(x) + '0')
new_df["Doctor_Activate"] = [True] * df.shape[0]
new_df = new_df.set_index(["Doctor_First_Name"])
new_df = new_df.sort_values("Doctor_Email").iloc[28:33, :]
print(new_df.info())
print(new_df)
new_df.to_csv("Doctor_data_C2.csv")
