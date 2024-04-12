"""
@Date    : 2024/4/8
@Author  : WangSun
@Version : 1.0
@Desc    : 双线性插值算法
"""

import numpy as np
import cv2

def bilinear_interpolation(src_img, dest_img):
    src_h, src_w = src_img.shape[0], src_img.shape[1]
    dest_h, dest_w = dest_img.shape[0], dest_img.shape[1]
    if src_h == dest_h and src_w == dest_w: # 图像大小相同直接复制
        return src_img.copy()
    for i in range(3): # 对每个通道进行循环
        for dest_y in range(dest_h): # 按行循环
            for dest_x in range(dest_w): # 按列循环

                # 0.5 为固定平移值
                src_x = (dest_x + 0.5) * src_w / dest_w - 0.5 # 几何中心靠近： x 方向进行平移
                src_y = (dest_y + 0.5) * src_h / dest_h - 0.5 # 几何中心靠近： y 方向进行平移

                # 取最近四个点的值
                src_x0 = int(np.floor(src_x))  # 向下取整
                src_x1 = min(src_x0 + 1, src_w - 1) # src_w-1 为列边界，不能越界
                src_y0 = int(np.floor(src_y))  # 行
                src_y1 = min(src_y0 + 1, src_h - 1) # src_h - 1 为行边界

                # 公式计算
                tmp0 = (src_x1 - src_x) * src_img[src_y0, src_x0, i] + (src_x - src_x0) * src_img[src_y0, src_x1, i]
                tmp1 = (src_x1 - src_x) * src_img[src_y1, src_x0, i] + (src_x - src_x0) * src_img[src_y1, src_x1, i]
                dest_img[dest_y, dest_x, i] = (src_y1 - src_y) * tmp0 + (src_y - src_y0) * tmp1

    return dest_img

src_img = cv2.imread("lenna.png")
dest_img = np.zeros((800, 800, 3), np.uint8)
dest_img = bilinear_interpolation(src_img, dest_img)
cv2.imshow("src_img", src_img)
cv2.imshow("dest_img", dest_img)
cv2.waitKey(0)