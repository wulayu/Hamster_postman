import numpy as np

import cv2

path = 'thumbnail.jpg'

img = cv2.imread(path)

# the image height

sum_rows = img.shape[0]

# the image length

sum_cols = img.shape[1]

part1 = img[0:sum_rows, 0:sum_cols // 2]

part2 = img[0:sum_rows, sum_cols // 2:sum_cols]

cv2.imshow('part1', part1)

cv2.imshow('part2', part2)

cv2.waitKey()

cv2.imwrite('1_1.jpg', part1)

cv2.imwrite('1_2.jpg', part2)
