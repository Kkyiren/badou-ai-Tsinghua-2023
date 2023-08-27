import cv2
import random

import numpy as np


def gaussian_noise(img_src: np.ndarray, mean, sigma, percent):
    """
    高斯噪声
    含义：利用服从高斯分布的概率密度的数值+上原有的像素点,范围[0,255]
    """
    new_img = img_src.copy()
    noise_number = int(img_src.shape[0] * img_src.shape[1] * percent)
    for i in range(noise_number):
        # 每次取一个随机点
        # 把一张图片的像素用行和列表示的话，randX 代表随机生成的行，randY代表随机生成的列
        # random.randint生成随机整数
        # 高斯噪声图片边缘不处理，故-1
        rand_x = random.randint(0, new_img.shape[0] - 1)
        rand_y = random.randint(0, new_img.shape[1] - 1)
        # 此处在原有像素灰度值上加上高斯分布随机数
        new_img[rand_x, rand_y] = new_img[rand_x, rand_y] + random.gauss(mean, sigma)
        # 若灰度值小于0则强制为0，若灰度值大于255则强制为255
        if new_img[rand_x, rand_y] < 0:
            new_img[rand_x, rand_y] = 0
        if new_img[rand_x, rand_y] > 255:
            new_img[rand_x, rand_y] = 255

    return new_img


if __name__ == '__main__':
    img = cv2.imread(r'../file/lenna.png')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = gaussian_noise(img_gray, mean=2, sigma=4, percent=0.8)
    cv2.imshow(" gaussion ", img_gaussian)
    cv2.imshow(" src ", img_gray)
    cv2.waitKey(10000)

    pass

