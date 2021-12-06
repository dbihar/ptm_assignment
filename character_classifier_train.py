import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from sklearn.utils import class_weight

#from sklearn.model_selection import train_test_split
import argparse

if __name__ == '__main__':
    import os
    import sys
    os.chdir(sys.path[0])
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(debug = False)
    parser.add_argument('--debug', dest = "debug", help='Program will print and plot relevant data', action='store_true')
    args = parser.parse_args()

    IMG_SIZE=32

    # Loading our data.
    #color_mode='grayscale'
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        "Data/Train3", image_size=(IMG_SIZE, IMG_SIZE), batch_size=1, color_mode='grayscale'
    )

    validation = tf.keras.preprocessing.image_dataset_from_directory(
        "Data/Validation", image_size=(IMG_SIZE, IMG_SIZE), batch_size=1, color_mode='grayscale'
    )

    # Data
    x_train, y_train = (zip(*dataset))
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train, y_train = np.squeeze(x_train), np.squeeze(y_train)

    # Validation
    x_test, y_test = (zip(*validation))
    x_test, y_test = np.array(x_test), np.array(y_test)
    x_test, y_test = np.squeeze(x_test), np.squeeze(y_test)

    #x_train, x_test, y_train, y_test = train_test_split(x_test, y_test,
    #                                                    test_size = 0.2,
    #                                                    random_state = 1)

    print("Data = ", x_train.shape, y_train.shape, "Val = ", x_test.shape, y_test.shape)

    if(args.debug):
        import matplotlib.pyplot as plt
        #Preview data

        class_names = validation.class_names
        plt.figure(figsize=(10, 10))

        start_im = 100
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(x_train[i + start_im])
            plt.title(class_names[y_train[i + start_im]])
            plt.axis("off")
        plt.show()

    # Normalizing
    x_train = tf.keras.utils.normalize(x_train, axis = 1)
    x_test = tf.keras.utils.normalize(x_test, axis = 1)

    class_names = ['0', "1", '(', ')', '+', '-', '/', 'x', '2', '3', '4', '5', '6', '7', '8', '9']

    #Normalize data prewiev
    if(args.debug):
        #class_names = dataset.class_names
        plt.figure(figsize=(10, 10))
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(x_train[i])
            plt.title(class_names[y_train[i]])
            plt.axis("off")
        plt.show()


    # Resizing
    x_trainr = np.array(x_train).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    x_testr = np.array(x_test).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    print("Training Samples dimension", x_trainr.shape)
    print("Testing Samples dimension", x_testr.shape)

    # Creating neural network
    # Creating the network
    model = Sequential()

    ### First Convolution Layer
    # 64 -> number of filters, (3,3) -> size of each kernal,
    model.add(Conv2D(32, (3,3), input_shape = x_trainr.shape[1:])) # For first layer we have to mention the size of input
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    ### Second Convolution Layer
    model.add(Conv2D(64, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    ### Third Convolution Layer
    model.add(Conv2D(256, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    ### Fully connected layer 1
    model.add(Flatten())
    model.add(Dense(64)) 
    model.add(Activation("relu"))

    ### Fully connected layer 2
    model.add(Dense(32))
    model.add(Activation("relu"))

    ### Fully connected layer 3, output layer must be equal to number of classes
    model.add(Dense(16))
    model.add(Activation("softmax"))
    
    model.summary()
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
    #model.fit(x_trainr, y_train, epochs=4, validation_split = 0.3)

    class_weights = class_weight.compute_class_weight(
                                        class_weight = "balanced",
                                        classes = np.unique(y_train),
                                        y = y_train                                                    
                                    )
    class_weights = dict(zip(np.unique(y_train), class_weights))

    print("Weights", class_weights, " Keys ", class_weights.keys())
    #x = {6:0}
    #x.update(class_weights)
    #class_weights = x
    model.fit(x_trainr, y_train, epochs=4, validation_split = 0.2, class_weight=class_weights)

    test_loss, test_acc = model.evaluate(x_testr, y_test)
    print("Test Loss on test samples", test_loss)
    print("Test Accuracy on test samples", test_acc)

    #Predictions

    # Saving a Keras model:
    model.save('Model')

    #Running metrics
    from sklearn.metrics import ConfusionMatrixDisplay
    from sklearn.metrics import confusion_matrix
    import matplotlib.pyplot as plt

    y_pred = model.predict(x_test)
    y_pred = [np.argmax(pred) for pred in y_pred]
    labels = ['0', "1", '(', ')', '+', '-', '/', 'x', '2', '3', '4', '5', '6', '7', '8', '9']

    cm = confusion_matrix(y_test, y_pred)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    disp.plot(cmap=plt.cm.Blues)
    plt.show()
