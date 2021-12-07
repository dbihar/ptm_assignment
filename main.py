#!/usr/bin/env python3
#
#   Main functionality of the program and it's procedures are connected here
#

from matplotlib import image
from expression_calculator import eval_expression_string, eval_expression_list
from character_separator import separate_characters
import cv2
import numpy as np
from character_classifier_detect import classify_image
from tensorflow import keras

IMG_SIZE = 32

def calculate(img):
    global IMG_SIZE
    
    # Separate characters
    characters = separate_characters(img, IMG_SIZE = 32, save_characters = True, debug = False)

    # Loading model
    model = keras.models.load_model('Model')

    # Getting expression
    expression = ""
    for character_im in characters:
        expression = expression + classify_image(character_im, model, IMG_SIZE, debug = False)
    
    # Evaluating expression
    print("Expression = ", expression)
    sol = eval_expression_string(expression)
    print("Solution = ", sol)
    return sol, expression