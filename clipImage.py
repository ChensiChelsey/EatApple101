import PIL.ImageOps
import numpy as np
import cv2
import scipy.misc
from scipy.misc import imsave
from PIL import Image, ImageDraw

input = "eq29" #set the name of image
im = cv2.imread("./test_image/" + input + ".png")

# convert the image into white and black image
im[im >= 127] = 255
im[im < 127] = 0

# set the morphology kernel size, the number in tuple is the bold pixel size
kernel = np.ones((3,3),np.uint8)
im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)

# make a tmpelate image for next crop
image = Image.fromarray(im)
image.save("temp.png")

# create grey image for retrieving contours
imgrey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgrey, 127, 255, 0)
im2, contours, hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # RETR_EXTERNAL for only bounding outer box

# bounding rectangle outside the individual element in image
num = 1
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    # exclude the whole size image
    if x is 0: continue
    # save rectangled element
    symbolImage = image.crop((x, y, x+w, y+h))
    symbolImage.save("./image/" + input + "_" + str(num) + "_" + str(y) + "_" + str(y+h) + "_" + str(x) + "_" + str(x+w) + ".png")
    # fill the found part with black to reduce effect to other crop
    draw = ImageDraw.Draw(image)
    draw.rectangle((x, y, x+w, y+h), fill = 'black')
    # draw rectangle around element in image for confirming result
    cv2.rectangle(im, (x,y), (x+w, y+h), (0,255,0), 2)
    num = num + 1
    
# save bouding result
image = Image.fromarray(im)    
image.save("boudingResult" + input + ".png")
