from matplotlib import image
from expression_calculator import eval_expression_string, eval_expression_list

from character_separator import separate_characters
import cv2
import numpy as np
from character_classifier_detect import classify_image
from tensorflow import keras

def calculate(img):
    print(type(img))

    characters = separate_characters(img, IMG_SIZE = 32, save_characters = True, debug = True)

    #Loading model
    model = keras.models.load_model('Model')

    expression = ""
    for character_im in characters:
        expression = expression + classify_image(character_im, model)
    
    print("Expression = ", expression)
    print("Solution = ", eval_expression_string(expression))