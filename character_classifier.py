import tensorflow as tf
import numpy as np

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

x_train = tf.keras.utils.normalize(x_train, axis = 1)
x_test = tf.keras.utils.normalize(x_test, axis = 1)
plt.imshow(x_train[115], cmap = plt.cm.binary)
plt.show()
print(y_train[115])