import PIL.Image
import numpy as np
# import pandas as pd


def sigmoid(inpt):
    return 1.0 / (1.0 + np.exp(-1 * inpt))


def relu(inpt):
    result = inpt
    result[inpt < 0] = 0
    return result


def predict_output(weights_mat_path, data_inputs, activation="relu"):
    weights_mat = np.load(weights_mat_path, allow_pickle=True)  # allow_pickle=True
    r1 = data_inputs
    for curr_weights in weights_mat:
        r1 = np.matmul(r1, curr_weights)
        if activation == "relu":
            r1 = relu(r1)
        elif activation == "sigmoid":
            r1 = sigmoid(r1)
    r1 = r1[0, :]
    predicted_label = np.where(r1 == np.max(r1))[0][0]
    class_labels = ["sweetpotato", "jjampong", "salad", "toast"]
    predicted_class = class_labels[predicted_label]
    return predicted_class


def extract_features(img_path):
    im = PIL.Image.open(img_path).convert("HSV")
    fruit_data_hsv = np.asarray(im, dtype=np.uint8)

    indices = np.load(file="indexx.npy")
    # indices  = np.load(file="indices.npy")

    hist = np.histogram(a=fruit_data_hsv[:, :, 0], bins=600)
    im_features = hist[0][indices]
    img_features = np.zeros(shape=(1, im_features.size))
    img_features[0, :] = im_features[:im_features.size]
    return img_features