import cv2
import numpy as np


def fac(img, out_dim):
    src_h, src_w, c = img.shape
    dst_h, dst_w = out_dim[1], out_dim[0]
    print("src_h, src_w = ", src_h, src_w)
    print("dst_h, dst_w = ", dst_h, dst_w)
    if src_h == dst_h and src_w == dst_w:
        return img.copy()
    dst_img = np.zeros((dst_h, dst_w, 3), dtype=np.uint8)
    scale_x, scale_y = float(src_w) / dst_w, float(src_h) / dst_h
    for i in range(3):
        for dst_y in range(dst_h):
            for dst_x in range(dst_w):
                src_x = (dst_x + 0.5) * scale_x - 0.5
                src_y = (dst_y + 0.5) * scale_y - 0.5
                src_x0 = int(np.floor(src_x))
                src_x1 = min(src_x0 + 1, src_w - 1)  # 为了避免像素坐标越界 因为图像坐标是从零开始的，所以范围为0-511，故为 src_w - 1
                src_y0 = int(np.floor(src_y))
                src_y1 = min(src_y0 + 1, src_h - 1)  # 为了避免像素坐标越界 因为图像坐标是从零开始的，所以范围为0-511，故为 src_h - 1
                temp0 = (src_x1 - src_x) * img[src_y0, src_x0, i] + (src_x - src_x0) * img[src_y0, src_x1, i]
                temp1 = (src_x1 - src_x) * img[src_y1, src_x0, i] + (src_x - src_x0) * img[src_y1, src_x1, i]
                dst_img[dst_y, dst_x, i] = int((src_y - src_y0) * temp1 + (src_y1 - src_y) * temp0)
    return dst_img


if __name__ == '__main__':
    img1 = cv2.imread("lenna.png")
    dst = fac(img1, (700, 700))
    cv2.imshow('bi-linear interp', dst)
    cv2.waitKey(0)
