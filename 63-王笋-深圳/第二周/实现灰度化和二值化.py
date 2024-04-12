# -*- coding: utf-8 -*-
"""
@author: WangSun

彩色图像的灰度化、二值化
"""
import cv2
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from PIL import Image
import numpy as np

# 灰度化
# 读取图片，cv2读取默认是BGR
img = cv2.imread('lenna.png')
# BGR转换为RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# 获取图片的高度和宽度
h,w = img.shape[:2]
# 创建一张和当前图片大小一样的单通道图片
img_gray = np.zeros([h,w],img.dtype)
# 实现灰度化
# img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # 调用方法库最简单
for i in range(h):
    for j  in range(w):
        m = img[i,j]  # 取出当前高度和宽度中的RGB坐标
        # RGB转化为Gray  浮点算法：Gray = R0.3 + G0.59 + B0.11
        # img_gray[i,j] = rgb2gray(m)
        img_gray[i,j] = int(m[0]*0.3 + m[1]*0.59 + m[2]*0.11)

print(m)
print(img_gray)
print('image show gray:',img_gray)
cv2.imshow('image show gray',img_gray)

plt.subplot(221)
img = plt.imread("lenna.png")
plt.imshow(img)
print('----image lenna------')
print(img)

# 灰度化
img_gray = rgb2gray(img)
plt.subplot(222)
plt.imshow(img_gray, cmap = 'gray')
print('-----image gray------')
print(img_gray)

# 二值化
rows, cols = img_gray.shape
# for i in range(rows):
#     for j in range(cols):
#         if(img_gray[i,j] <= 0.5):
#             img_gray[i,j] = 0
#         else:
#             img_gray[i,j] = 1

img_binary = np.where(img_gray >= 0.5, 1, 0)
print("-----imge_binary-------")
print(img_binary)
print(img_binary.shape)

plt.subplot(223)
plt.imshow(img_binary, cmap='binary')
plt.show()