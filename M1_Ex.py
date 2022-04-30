import matplotlib.pylab as plt
import cv2

import numpy as np
#Importar e converter a imagem em preto e branco (diminui a complexidade da imagem)
img = cv2.imread("road.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(gray)
plt.show()

#Regular a escala de cinzentos aplicada a imagem (reduz o ruido da imagem)
blur = cv2.Gaussianblur(gray, (5,5), 0)
plt.imshow(blur,cmap='gray')
plt.title('GausssianBlur'), plot.xticks([]), plot.yticks([])
plt.show()

#Detetar a estrada
edges = cv2.Canny(img,100,200)
plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plot.xticks([]), plot.yticks([])
plt.show()

#Definir área a considerar
def region(image):
    height, width = image.shape
    triangle = np.array([
        [(100, height), (475, 325), (width, height)]
    ])

    mask = np.zeros_like(image)

    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

#Marcar as linhas de estrada
lines: object = cv2.HoughLinesP(isolated, rho=2, theta=np.pi/180, threshold=100, np.array([]), minLineLength=40, maxLineGap=5)

#Calcular a inclinação média das linhas da estrada
def average(image, lines):
    left = []
    right = []
    for line in lines:
        print(line)