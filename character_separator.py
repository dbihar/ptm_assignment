import cv2 
import numpy as np
import imutils
import argparse
import os

#resize but doesnt distort vertical aspect ratio
def resize_image(img, size=(32,32)):

    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape)>2 else 1
    #print(h,w)
    
    if h > w * 2.8: 
        print("Extreme slender")
        img = cv2.resize(img, (15,29), cv2.INTER_NEAREST)
        h, w = img.shape[:2]
        new_image_width = 32
        new_image_height = 32
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
        img = cv2.resize(img, (25,29), cv2.INTER_NEAREST)
        h, w = img.shape[:2]
        new_image_width = 32
        new_image_height = 32
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

    new_image_width = 15
    new_image_height = 32
    color = (0)
    result = np.full((new_image_height,new_image_width), color, dtype=np.uint8)

    # compute center offset
    x_center = (new_image_width - w) // 2
    y_center = (new_image_height - h) // 2

    # copy img image into center of result image
    result[y_center:y_center+h, x_center:x_center+w] = img
    result = cv2.resize(result, (32,32), cv2.INTER_NEAREST)
    return result

def separate_characters(image, IMG_SIZE = 32, save_characters = False, debug = False):
    print("Image_type:", type(image), " Shape:", image.shape)
    PATH = 'Characters'
    #image = imutils.resize(image, height = 1000)
    image = imutils.resize(image, height = 400)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(gray, 13)
    thresh = cv2.adaptiveThreshold(blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV,51,4)
    
    if(debug):
        cv2.imshow('tresh ', thresh)
        key = cv2.waitKey(200)
        #cv2.imshow('gr ', image)
        #key = cv2.waitKey(200)
        #cv2.imshow('im ', gray)
        #key = cv2.waitKey(200)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3)) #Tune this to get good separation
    dilate = cv2.dilate(thresh, kernel, iterations=30)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ROI_list = []

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            im_tmp = thresh[y:y+h, x:x+w]
            _, im_tmp = cv2.threshold(im_tmp, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            ROI = im_tmp, x 

            ROI_list.append(ROI)

    ROI_in_order = sorted(ROI_list, key=lambda tup: tup[1])

    if(save_characters):
        dir = 'Characters'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        for ROI, x in ROI_in_order:
            cv2.imwrite(os.path.join(PATH , 'ch_at_' + str(x) + ".jpg"), resize_image(ROI, (IMG_SIZE,IMG_SIZE)))
            
    ROI_list = list(ROI_in_order)
    #print(ROI_list)
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
    IMG_SIZE = 32

    PATH = 'Characters'
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(path = "img3.jpg")
    parser.add_argument( 'path', action = 'store', type = str, help = 'Path to image file.' )
    args = parser.parse_args()

    print(args.path)
    image = cv2.imread(args.path)
    image = imutils.resize(image, height = 400)

    #(thresh, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.medianBlur(gray, 13)
    thresh = cv2.adaptiveThreshold(blur, 255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV,51,4)
    cv2.imshow('tresh ', thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3)) #This kernel is to catch slender - sign
    dilate = cv2.dilate(thresh, kernel, iterations=30)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ROI_list = []

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            #ROI = gray[y:y+h, x:x+w], x
            im_tmp = thresh[y:y+h, x:x+w]
            (_, im_tmp) = cv2.threshold(im_tmp, 127, 255, cv2.THRESH_BINARY)
            ROI = im_tmp, x
            ROI_list.append(ROI)
            #print(ROI_list)

    ROI_list = [(cv2.blur((resize_image(item[0], (IMG_SIZE,IMG_SIZE))), (2,2)), item[1]) for item in ROI_list]
    ROI_in_order = sorted(ROI_list, key=lambda tup: tup[1])

    
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

    """
    img_gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    img_gauss = cv2.GaussianBlur(img_gray, (3,3), 0)
    kernel = np.ones((4,4), np.uint8) 
    erode = cv2.erode(img_gauss, kernel, iterations=1)
    th3 = cv2.adaptiveThreshold(erode,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,10)
    ctrs, hier = cv2.findContours(th3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    rects.sort()
    """
    #x, y, w, h = rects[0]
    #cv2.rectangle(ROI, (x, y), (x+w, y+h), (0, 255, 0), 3)
    #cv2.imshow('Window_name', ROI)
    #key = cv2.waitKey(3000)