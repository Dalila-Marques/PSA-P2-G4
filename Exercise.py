""" 
ENUNCIADO: 
Criar um script python para, lendo uma imagem de estrada retirada do google 
do disco local, decidir para onde virar e mostrar esta decisão ao utilizador. 
"""



#Imports

import cv2
from cv2 import addWeighted
import numpy as np
import matplotlib.pyplot as plt


# Get image

img = cv2.imread('Turn.png')

"""plt.figure(figsize=(15,10))
plt.title('Image')
plt.imshow(img)
plt.show()"""

# Pre-processing image

# Grayscaling

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

"""plt.figure(figsize=(15,10))
plt.title('Gray Image')
plt.imshow(gray)
plt.show()"""


#Apply masking region to the image

img_hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)

lower_yellow = np.array([20,120,80], dtype = 'uint8')
upper_yellow = np.array([45,200,255], dtype = 'uint8')

mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

mask_white = cv2.inRange(gray, 200, 255)

mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
mask_yw_img = cv2.bitwise_and(gray, mask_yw)

"""plt.figure(figsize=(15,10))
plt.imshow(mask_yw_img)
plt.title('Masked Image')"""

# Applying gaussian blur - non necessary bc canny already does this

blur = cv2.GaussianBlur(mask_yw_img, (5,5), 0)

"""plt.figure(figsize=(15,10))
plt.title('Blurred Image')
plt.imshow(blur)
plt.show()"""

# Apply canny edge detection to the image

edges = cv2.Canny(blur, 50, 150)

"""plt.figure(figsize=(15,10))
plt.title('Edges')
plt.imshow(edges)
plt.show()"""

# Defining a ROI

stencil = np.zeros_like(mask_yw_img)

height = img.shape[0]

polygon = np.array([[500, height], [600, 400], [1300, 400], [1500, height]])

cv2.fillPoly(stencil, [polygon], 255)

"""plt.figure(figsize=(15,10))
plt.imshow(stencil, cmap="gray")
plt.title('Apllied ROI')
plt.show()"""

# Applying the defined ROI

ROI_img = cv2.bitwise_and(edges, stencil) 

plt.figure(figsize=(15,10))
plt.imshow(ROI_img)
plt.title('ROI Image')
plt.show()

# Apply Houghlines

lines = cv2.HoughLinesP(ROI_img, 7, np.pi/180, 100, np.array([]), minLineLength=75, maxLineGap=20)

detected_lines = np.zeros_like(img)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(detected_lines, (x1, y1), (x2, y2), (255, 0, 0), 3)

line_img = addWeighted(img, 0.8, detected_lines, 1, 1)

plt.figure(figsize=(15,10))
plt.imshow(detected_lines)
plt.title('Detected lines')
plt.show()
plt.figure(figsize=(15,10))
plt.imshow(line_img)
plt.title('Detected lines')
plt.show()

# Extrapolate the lines found in the hough transform to construct the left and right lane lines
# Add the extrapolated lines to the input image


