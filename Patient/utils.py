import pickle
import os
import numpy as np

# pickled objects file paths
MODEL_FILE_PATH = os.path.join("Pickles", "model_Symptomata_de_Morbo.pkl")
SYMPTOMS_FILE_PATH = os.path.join("Pickles", "symptom_labels.pkl")
DISEASE_LABELS_FILE_PATH = os.path.join("Pickles", "Disease_Labels.pkl")

# load pickled objects
with open(MODEL_FILE_PATH, mode="rb") as f:
    model = pickle.load(f)
with open(SYMPTOMS_FILE_PATH, mode="rb") as f:
    symptoms_list = pickle.load(f).tolist()
    print(len(symptoms_list))
with open(DISEASE_LABELS_FILE_PATH, mode="rb") as f:
    disease_labels = pickle.load(f)


def get_disease_labels():
    return disease_labels


def get_model():
    return model


def get_symptom_labels():
    return symptoms_list


def predict(inputs):
    # input: list of strings
    # get indices
    input_indices = [symptoms_list.index(x) for x in inputs]
    # multi hot input
    model_inputs = [[0] * len(symptoms_list)]
    for i in input_indices:
        model_inputs[0][i] = 1
    print(model_inputs)
    # predict
    y_pred = model.predict(np.array(model_inputs))[0]
    # zip with disease label
    return dict(zip(disease_labels, y_pred))
