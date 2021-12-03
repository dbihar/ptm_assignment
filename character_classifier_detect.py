import tensorflow as tf
import numpy as np
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

IMG_SIZE=32


#Loading model
from tensorflow import keras
model = keras.models.load_model('Model')

validation = tf.keras.preprocessing.image_dataset_from_directory(
    "Data/Validation", image_size=(32, 32), batch_size=1, color_mode='grayscale'
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
plt.figure(figsize=(10, 10))
start_im = 100
for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(x_test[i + start_im])
    plt.title(class_names[np.argmax(predictions[i + start_im])])
    plt.axis("off")
plt.show()

#plt.imshow(x_test[0])
#print(np.argmax(predictions[0]))


#Predicting arbitrary img
"""
import cv2
img = cv2.imread('three.png')
plt.imshow(img)

img.shape
# (28, 28, 3)

# Converting to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray.shape
# (28, 28)

# Resizing to a 28x28 image
# Please note my image was already in correct dimension
resized = cv2.resize(gray, (28,28), interpolation = cv2.INTER_AREA)
resized.shape
# (28, 28)

# 0-1 scaling
newimg = tf.keras.utils.normalize(resized, axis = 1)

# For kernal operations
newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

newimg.shape
# (1, 28, 28, 1)

predictions = model.predict(newimg)
print(np.argmax(predictions[0]))
# 3
"""