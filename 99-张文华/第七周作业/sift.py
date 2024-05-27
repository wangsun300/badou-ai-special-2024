'''
实现SIFT
'''

import cv2

img = cv2.imread('lenna.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()

keypoints, descriptor = sift.detectAndCompute(img_gray, None)
img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints,
                        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                        color=(255, 255, 255))

cv2.imshow('sift_keypoints', img)
cv2.waitKey(0)
cv2.destroyAllWindows()