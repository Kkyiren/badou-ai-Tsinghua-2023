import numpy as np
from numpy import shape
import random
import cv2


# 高斯噪声
def GaussianNoise(src, means, sigma, percetage):
    NoiseImg = src
    NoiseNum = int(percetage * src.shape[0] * src.shape[1])
    for i in range(NoiseNum):
        randX = random.randint(0, src.shape[0] - 1)
        randY = random.randint(0, src.shape[1] - 1)
        NoiseImg[randX, randY] = NoiseImg[randX, randY] + random.gauss(means, sigma)
        if NoiseImg[randX, randY] < 0:
            NoiseImg[randX, randY] = 0
        elif NoiseImg[randX, randY] > 255:
            NoiseImg[randX, randY] = 255
    return NoiseImg


# 椒盐噪声
def SPNoise(src, percetage):
    NoiseImg = src
    NoiseNum =int(percetage * src.shape[0] * src.shape[1])
    for i in range(NoiseNum):
        randX = random.randint(0, src.shape[0]-1)
        randY = random.randint(0, src.shape[1]-1)
        if random.random() <= 0.5:
            NoiseImg[randX, randY] = 0
        else:
            NoiseImg[randX, randY] = 255
    return NoiseImg


# 实现高斯噪声
img = cv2.imread('lenna.png', 0)
img1 = GaussianNoise(img, 2, 4, 0.8)

# 实现椒盐噪声
img = cv2.imread('lenna.png', 0)
img3 = SPNoise(img, 0.2)

img = cv2.imread('lenna.png')
img2 =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('source', img2)
cv2.imshow('lenna_PepperandSalt', img3)
cv2.imshow('lenna_GaussianNoise', img1)
cv2.waitKey(0)
