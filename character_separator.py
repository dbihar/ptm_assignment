import cv2 
import numpy as np
import imutils
from google.colab.patches import cv2_imshow

#pip3 install google-colab

image = cv2.imread("img.jpg")
image = imutils.resize(image, height = 500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
cv2.THRESH_BINARY_INV,11,8)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=10)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    area = cv2.contourArea(c)
    if area > 500:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+w]
        cv2_imshow(ROI)
        break

img_gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
img_gauss = cv2.GaussianBlur(img_gray, (3,3), 0)
kernel = np.ones((4,4), np.uint8) 
erode = cv2.erode(img_gauss, kernel, iterations=1)
th3 = cv2.adaptiveThreshold(erode,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,10)
im_th2, ctrs, hier = cv2.findContours(th3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
rects = [cv2.boundingRect(ctr) for ctr in ctrs]
rects.sort()

x, y, w, h = rects[0]
cv2.rectangle(ROI, (x, y), (x+w, y+h), (0, 255, 0), 3)
cv2_imshow(ROI)