import pickle
import os
import numpy as np

# pickled objects file paths
MODEL_FILE_PATH = os.path.join("Pickles", "model_Morbus_Praedictum_v5.pkl")
SYMPTOMS_FILE_PATH = os.path.join("Pickles", "symptoms_stoi.pkl")
DISEASE_LABELS_FILE_PATH = os.path.join("Pickles", "diseases_stoi.pkl")

# load pickled objects
with open(MODEL_FILE_PATH, mode="rb") as f:
    model = pickle.load(f)
with open(SYMPTOMS_FILE_PATH, mode="rb") as f:
    symptoms_stoi = pickle.load(f)
with open(DISEASE_LABELS_FILE_PATH, mode="rb") as f:
    diseases_stoi = pickle.load(f)


def predict(inputs):
    # input: list of strings
    # get indices
    input_indices = [symptoms_stoi[x] for x in inputs]
    # multi hot input
    model_inputs = [[0] * len(symptoms_stoi.keys())]
    for i in input_indices:
        model_inputs[0][i] = 1
    # predict
    y_pred = model.predict(np.array(model_inputs))[0]
    # zip with disease label
    return dict(zip(diseases_stoi, y_pred))
