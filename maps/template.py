import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('map.png')
l = [120, 30, 20]
u = [180, 90, 80]

lower = np.array(l, dtype = 'uint8')
upper = np.array(u, dtype = 'uint8')
mask = cv2.inRange(img_rgb, lower, upper)
output = cv2.bitwise_and(img_rgb, img_rgb, mask = mask)

img_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
template = cv2.imread('temp_filter.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
print loc
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
cv2.imwrite('out.png',output)

''' Blue symbols: 51, 60, 148
Red symbols: 197, 57, 54
Green symbols: 31, 168, 79
Orange: 239, 130, 90'''