import tensorflow as tf
import numpy as np
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

import argparse

def get_class_names():
    class_names = ['0', '1', '(', ')', '+', '-', '', '/', '×', '2', '3', '4', '5', '6', '7', '8', '9']
    return class_names

def classify_image(img, model, IMG_SIZE = 32):
    #import cv2
    #img = cv2.imread('three.png')
    #plt.imshow(img)

    # Converting to grayscale
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resizing to a 32x32 image
    # Please note my image was already in correct dimension
    #resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)
 
    # 0-1 scaling
    newimg = tf.keras.utils.normalize(img, axis = 1)
    normalized_img = newimg

    # For kernal operations
    newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    predictions = model.predict(newimg)
    class_names = get_class_names()
    print("predict = ",class_names[np.argmax(predictions[0])])


    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow((img))
    plt.title(class_names[np.argmax(predictions[0])])
    plt.axis("off")
    plt.show()

    plt.figure()
    plt.imshow(np.squeeze(normalized_img))
    plt.title(class_names[np.argmax(predictions[0])])
    plt.axis("off")
    plt.show()

    return (class_names[np.argmax(predictions[0])])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(debug = False)
    parser.add_argument('--debug', dest = "debug", help='Program will print and plot relevant data', action='store_true')
    args = parser.parse_args()

    IMG_SIZE=32


    #Loading model
    from tensorflow import keras
    model = keras.models.load_model('Model')

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


        import matplotlib.pyplot as plt
        #Preview data

        class_names = validation.class_names
        class_names[class_names.index("10")] = "("
        class_names[class_names.index("11")] = ")"
        class_names[class_names.index("12")] = "+"
        class_names[class_names.index("13")] = "-"
        class_names[class_names.index("14")] = ""
        class_names[class_names.index("15")] = "/"
        class_names[class_names.index("16")] = "x"

        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 10))
        start_im = 0
        for j in range(10):
            start_im = start_im + 9
            for i in range(9):
                ax = plt.subplot(3, 3, i + 1)
                plt.imshow(x_test[i + start_im])
                plt.title(class_names[np.argmax(predictions[i + start_im])])
                plt.axis("off")
            plt.show()
 
    #plt.imshow(x_test[0])
    #print(np.argmax(predictions[0]))

    else:
        class_names = ['0', '1', '(', ')', '+', '-', '', '/', 'x', '2', '3', '4', '5', '6', '7', '8', '9']

        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir("Characters") if isfile(join("Characters", f))]

        #Predicting arbitrary img
        import cv2
        import matplotlib.pyplot as plt

        print("File list = ", onlyfiles)
        for filename in onlyfiles:
            img = cv2.imread("Characters/" + filename)

            # Converting to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # gray.shape
 

            # Resizing to a 28x28 image
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