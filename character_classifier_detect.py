import tensorflow as tf
import numpy as np
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

IMG_SIZE=32


#Loading model
from tensorflow import keras
model = keras.models.load_model('Model')

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