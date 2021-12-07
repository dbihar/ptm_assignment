#!/usr/bin/env python3
#
#   Script classifies characters from ./Characters folder
#
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os, sys

from tensorflow import keras
from os import listdir
from os.path import isfile, join
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

IMG_SIZE=32

def get_class_names():
    class_names = ['0', "1", '(', ')', '+', '-', '/', 'x', '2', '3', '4', '5', '6', '7', '8', '9']
    return class_names

def classify_image(img, model, IMG_SIZE = 32, debug = False):
    # 0-1 scaling
    newimg = tf.keras.utils.normalize(img, axis = 1)
    normalized_img = newimg

    # For kernal operations
    newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    # Making model predictions 
    predictions = model.predict(newimg)
    class_names = get_class_names()
    
    if(debug):
        plt.figure()
        plt.imshow(np.squeeze(normalized_img))
        plt.title(class_names[np.argmax(predictions[0])])
        plt.axis("off")
        plt.show()

    return (class_names[np.argmax(predictions[0])])

if __name__ == '__main__':
    os.chdir(sys.path[0])
    
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(debug = False)
    parser.add_argument('--debug', dest = "debug", help='Program will print and plot relevant data', action='store_true')
    args = parser.parse_args()

    #Loading model
    model = keras.models.load_model('Model')

    # If we want to predicti on validation dataset (for metrics etc.)
    validation_bool = False

    if(validation_bool):
        validation = tf.keras.preprocessing.image_dataset_from_directory(
            "Data/Validation", image_size=(IMG_SIZE, IMG_SIZE), batch_size=1, color_mode='grayscale'
        )
        x_test, y_test = (zip(*validation))
        x_test, y_test = np.array(x_test), np.array(y_test)
        x_test, y_test = np.squeeze(x_test), np.squeeze(y_test)
        x_test = tf.keras.utils.normalize(x_test, axis = 1)
        x_testr = np.array(x_test).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

        predictions = model.predict([x_testr])
        #print(predictions)

        #Preview data
        class_names = validation.class_names
        print("Class names", class_names)
        class_names[class_names.index("10")] = "("
        class_names[class_names.index("11")] = ")"
        class_names[class_names.index("12")] = "+"
        class_names[class_names.index("13")] = "-"
        class_names[class_names.index("14")] = "/"
        class_names[class_names.index("15")] = "x"

        plt.figure(figsize=(10, 10))
        start_im = 0
        for j in range(2):
            start_im = start_im + 9
            for i in range(9):
                ax = plt.subplot(3, 3, i + 1)
                plt.imshow(x_test[i + start_im])
                plt.title(class_names[np.argmax(predictions[i + start_im])])
                plt.axis("off")
            plt.show()
 
        # Running metrics
        y_pred = model.predict(x_test)
        y_pred = [np.argmax(pred) for pred in y_pred]
        labels = ['0', "1", '(', ')', '+', '-', '/', 'x', '2', '3', '4', '5', '6', '7', '8', '9']

        cm = confusion_matrix(y_test, y_pred)

        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

        disp.plot(cmap=plt.cm.Blues)
        plt.show()

    #
    # Predicting from "./Characters"
    #
    else: 
        class_names = get_class_names()
        onlyfiles = [f for f in listdir("Characters") if isfile(join("Characters", f))]

        #Predicting arbitrary img

        print("File list = ", onlyfiles)
        for filename in onlyfiles:
            img = cv2.imread("Characters/" + filename)

            # Converting to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Resizing to a 32x32 image
            # Please note my image was already in correct dimension
            resized = cv2.resize(gray, (32,32), interpolation = cv2.INTER_AREA)
            #resized.shape

            # 0-1 scaling
            newimg = tf.keras.utils.normalize(resized, axis = 1)
            plt.imshow(img)

            # For kernal operations
            newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

            predictions = model.predict(newimg)
            print(class_names[np.argmax(predictions[0])])
            plt.show()