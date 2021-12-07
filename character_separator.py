#!/usr/bin/env python3
#
#   Character separator functionality.
#   For image path input it divides Characters and saves them in ./Characters
#

import cv2 
import numpy as np
import imutils
import argparse
import os, sys

IMG_SIZE=32

#Resize but ajust aspect ratio to work best with ML model
def resize_image(img, size=(IMG_SIZE, IMG_SIZE)):

    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape)>2 else 1
    
    if h > w * 2.8: 
        print("Extreme slender")
        img = cv2.resize(img, (15,29), cv2.INTER_NEAREST)
        h, w = img.shape[:2]
        new_image_width = IMG_SIZE
        new_image_height = IMG_SIZE
        color = (0)
        result = np.full((new_image_height,new_image_width), color, dtype=np.uint8)

        # compute center offset
        x_center = (new_image_width - w) // 2
        y_center = (new_image_height - h) // 2

        # copy img image into center of result image
        result[y_center:y_center+h, x_center:x_center+w] = img
        return result

    if h > w: 
        print("Normal slender")
        img = cv2.resize(img, (24,31), cv2.INTER_NEAREST) #Play with aspect ration of letters
        h, w = img.shape[:2]
        new_image_width = IMG_SIZE
        new_image_height = IMG_SIZE
        color = (0)
        result = np.full((new_image_height,new_image_width), color, dtype=np.uint8)

        # compute center offset
        x_center = (new_image_width - w) // 2
        y_center = (new_image_height - h) // 2

        # copy img image into center of result image
        result[y_center:y_center+h, x_center:x_center+w] = img
        return result

    print("Wide character")
    fact = w / 25.
    w = 16
    h = int(float(h) / fact)
    img = cv2.resize(img, (w,h), cv2.INTER_NEAREST)

    new_image_width = 16
    new_image_height = 32
    color = (0)
    result = np.full((new_image_height,new_image_width), color, dtype=np.uint8)

    # compute center offset
    x_center = (new_image_width - w) // 2
    y_center = (new_image_height - h) // 2

    # copy img image into center of result image
    result[y_center:y_center+h, x_center:x_center+w] = img
    result = cv2.resize(result, (IMG_SIZE, IMG_SIZE), cv2.INTER_NEAREST)
    return result

def separate_characters(image, IMG_SIZE = 32, save_characters = False, debug = False):

    # Comments are the same as in main so brief version here

    print("Image_type:", type(image), " Shape:", image.shape)
    PATH = 'Characters'

    # Resizing to fixed height so that kernels function the same
    image = imutils.resize(image, height = 400)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising
    blur = cv2.medianBlur(gray, 13)
    thresh = cv2.adaptiveThreshold(blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV,51,4)
    
    if(debug):
        cv2.imshow('tresh ', thresh)
        key = cv2.waitKey(200)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3)) #Tune this to get good separation
    dilate = cv2.dilate(thresh, kernel, iterations=30)

    # Finding characters
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Splitting characters and populating list with their x coordinate
    ROI_list = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            im_tmp = thresh[y:y+h, x:x+w]
            _, im_tmp = cv2.threshold(im_tmp, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            ROI = im_tmp, x 

            ROI_list.append(ROI)

    # Sorting characters from left to right
    ROI_in_order = sorted(ROI_list, key=lambda tup: tup[1])

    # Saving characters
    if(save_characters):
        import os
        import sys
        os.chdir(sys.path[0])
        try:
            dir = 'Characters'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            for ROI, x in ROI_in_order:
                cv2.imwrite(os.path.join(PATH , 'ch_at_' + str(x) + ".jpg"), resize_image(ROI, (IMG_SIZE,IMG_SIZE)))
        except FileNotFoundError:
            print("[WARN] No Character directory")

    # Sorting characters from left to rigth      
    ROI_list = list(ROI_in_order)
    ROI_list = [cv2.blur((resize_image(item[0], (IMG_SIZE,IMG_SIZE))), (2,2)) for item in ROI_list] #Final blur off

    if(debug or save_characters):
        if(debug):
            stack = np.hstack(ROI_list)
            cv2.imshow('Character', stack)
            key = cv2.waitKey(1200)
        for ROI in ROI_list:
            if(save_characters):
                 cv2.imwrite(os.path.join(PATH , 'ch_at_' + str(x) + ".jpg"), ROI)

    return ROI_list

if __name__ == '__main__':
    os.chdir(sys.path[0])
    
    PATH = 'Characters'
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(path = "img3.jpg")
    parser.add_argument( 'path', action = 'store', type = str, help = 'Path to image file.' )
    args = parser.parse_args()

    # Load image
    print(args.path)
    image = cv2.imread(args.path)

    #Resizing so that we keep enough information but also that our kernels can work on any resolution input
    image = imutils.resize(image, height = 400)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising
    blur = cv2.medianBlur(gray, 13)
    thresh = cv2.adaptiveThreshold(blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV,51,4)
    cv2.imshow('tresh ', thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3)) #This kernel is to catch slender "-" sign
    dilate = cv2.dilate(thresh, kernel, iterations=30)

    # Finding characters
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Populating list of characters and their x position (Splitting characters)
    ROI_list = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            im_tmp = thresh[y:y+h, x:x+w]
            (_, im_tmp) = cv2.threshold(im_tmp, 127, 255, cv2.THRESH_BINARY)
            ROI = im_tmp, x
            ROI_list.append(ROI)

    # Sorting characters from left to right
    ROI_list = [(cv2.blur((resize_image(item[0], (IMG_SIZE,IMG_SIZE))), (2,2)), item[1]) for item in ROI_list]
    ROI_in_order = sorted(ROI_list, key=lambda tup: tup[1])

    # Saving to ./Characters folder
    save_characters = True
    if(save_characters):
        dir = 'Characters'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        for count, ROI_t in enumerate(ROI_in_order):
            ROI, x = ROI_t
            cv2.imwrite(os.path.join(PATH , 'ch' + str(count) + ".jpg"), ROI)
            
    ROI_list = [ROI for ROI, x in ROI_in_order]
    stack = np.hstack(ROI_list)
    cv2.imshow('Character', stack)
    key = cv2.waitKey(5000)