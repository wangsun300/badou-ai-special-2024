"""
@Date      : 2024/4/8
@Author    : WangSun
@Version   : 1.0
@Desc      : 直方图均衡化（图像增强）
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

'''
单通道图像均衡化
函数： equalizeHist(src, dst=None)
src:  图像矩阵（单通道图像）
dst:  默认即可
'''

# 获取灰度图像
img = cv2.imread('lenna.png',1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('image_gray', gray)

# 灰度图像直方图均衡化
dst = cv2.equalizeHist(gray)

# 直方图
hist = cv2.calcHist([dst], [0], None, [256], [0, 256])

plt.figure()  # 创建图形对象
plt.hist(dst.ravel(), 256)  # hist(): 绘制直方图，bins：表示将数据分成多少个区间， ravel() ：合成一元数组
plt.show()

cv2.imshow('Histogram Equalization', np.hstack([gray,dst]))
cv2.waitKey(0)  # waitKey()的基本逻辑,他会在一定时间内等待接收键盘上的一个值(都是在展示imshow后面使用),若参数delay≤0：表示一直等待按键


# 彩色图像直方图均衡化
img = cv2.imread('lenna.png', 1)
cv2.imshow('src', img)

# 彩色图像均衡化，需要分解通道   对每个通道均衡化
(b, g, r) = cv2.split(img)
bH = cv2.equalizeHist(b)
gH = cv2.equalizeHist(g)
rH = cv2.equalizeHist(r)

# 合并每一个通道
result = cv2.merge((bH, gH, rH))
cv2.imshow('dst_rgb', result)
cv2.waitKey(0)


