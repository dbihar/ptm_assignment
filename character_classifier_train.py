import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

IMG_SIZE=32

# Loading our data.
#color_mode='grayscale'
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "Data/Train", image_size=(32, 32), batch_size=1, color_mode='grayscale'
)

validation = tf.keras.preprocessing.image_dataset_from_directory(
    "Data/Validation", image_size=(32, 32), batch_size=1, color_mode='grayscale'
)

# Data
x_train, y_train = (zip(*dataset))
x_train, y_train = np.array(x_train), np.array(y_train)
x_train, y_train = np.squeeze(x_train), np.squeeze(y_train)

# Validation
x_test, y_test = (zip(*validation))
x_test, y_test = np.array(x_test), np.array(y_test)

x_test, y_test = np.squeeze(x_test), np.squeeze(y_test)

print("Data = ", x_train.shape, y_train.shape, "Val = ", x_test.shape, y_test.shape)


import matplotlib.pyplot as plt
#Preview data
"""
class_names = dataset.class_names
plt.figure(figsize=(10, 10))
for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i]])
    plt.axis("off")
plt.show()
"""
# Normalizing
x_train = tf.keras.utils.normalize(x_train, axis = 1)
x_test = tf.keras.utils.normalize(x_test, axis = 1)

#Normalize data prewiev
"""
class_names = dataset.class_names
plt.figure(figsize=(10, 10))
for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i]])
    plt.axis("off")
plt.show()
"""

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
model.add(Conv2D(64, (3,3), input_shape = x_trainr.shape[1:])) # For first layer we have to mention the size of input
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

### Second Convolution Layer
model.add(Conv2D(64, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

### Third Convolution Layer
model.add(Conv2D(64, (3,3)))
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
model.add(Dense(10))
model.add(Activation("softmax"))

model.summary()
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(x_trainr, y_train, epochs=1, validation_split = 0.3)

test_loss, test_acc = model.evaluate(x_testr, y_test)
print("Test Loss on 10,000 test samples", test_loss)
print("Test Accuracy on 10,000 test samples", test_acc)

#Predictions

predictions = model.predict([x_testr])
print(predictions)

plt.imshow(x_test[0])
print(np.argmax(predictions[0]))


#Saving_model
# Saving a Keras model:
model.save('Model')