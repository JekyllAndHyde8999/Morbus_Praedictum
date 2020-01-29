import pandas as pd
import datetime
import numpy as np

TOP_K = 11

blood_group_choices = list(range(1, 5))


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
                               "Patient_First_Name",
                               "Patient_Last_Name",
                               "Patient_Gender",
                               "Patient_DOB",
                               "Patient_Blood_Group",
                               "Patient_Blood_Donation",
                               "Patient_Email"])
new_df = new_df.set_index(["index"])

new_df["Patient_First_Name"] = df["Name"].apply(lambda x: x.split()[0])
new_df["Patient_Last_Name"] = df["Name"].apply(lambda x: x.split()[1])
new_df["Patient_Gender"] = df["Sex"].apply(getGender)
new_df["Patient_DOB"] = df["DOB"].apply(parseDates)
new_df["Patient_Blood_Group"] = [np.random.choice(blood_group_choices) for _ in range(df.shape[0])]
new_df["Patient_Blood_Donation"] = [False] * df.shape[0]
new_df["Patient_Email"] = df["Name"].apply(getEmail)
new_df = new_df.set_index(["Patient_First_Name"])
new_df = new_df.sort_values('Patient_Email').iloc[8:10, :]
print(new_df.info())
new_df.to_csv("Patient_data.csv")
