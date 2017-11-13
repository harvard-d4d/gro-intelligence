import cv2
import numpy as np
import os
import pandas as pd
from matplotlib import pyplot as plt

threshold = 0.8

def analyze(foldername, l, u):
	# Dictionary of points for pandas
	lst = {"image": [], "template": [], "pt0":[], "pt1":[]}

	# Go through the images collected
	for image in os.listdir('imgs'):
		# Ignore non-png files
		if image[-3:] != 'png': continue
		img_rgb = cv2.imread('imgs/' + image)

		lower = np.array(l, dtype = 'uint8')
		upper = np.array(u, dtype = 'uint8')

		# Threshold
		mask = cv2.inRange(img_rgb, lower, upper)

		# Scroll through templates
		for filename in os.listdir(foldername):
			# Ignore non-png files
			if filename[-3:] != 'png': continue
			template = cv2.imread(foldername + '/' + filename,0)
			w, h = template.shape[::-1]
			# Template matching
			res = cv2.matchTemplate(mask, template, cv2.TM_CCOEFF_NORMED)
			threshold = 0.8
			loc = np.where(res >= threshold)
			for pt in zip(*loc[::-1]):
				# Add to dictionary
				lst["image"].append(image)
				lst["template"].append(filename)
				lst["pt0"].append(pt[0])
				lst["pt1"].append(pt[1])
				cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
			# If you want to see found points, uncomment this
			# cv2.imwrite('res' + image + '.png', img_rgb)
	df = pd.DataFrame(lst)
	# Save as csv
	df.to_csv(foldername + ".csv")

# Function good for viewing mask
def output(l, u):
	for filename in os.listdir('imgs'):
		if (filename[-3:] == 'png'):
			img_rgb = cv2.imread('imgs/' + filename)
			lower = np.array(l, dtype = 'uint8')
			upper = np.array(u, dtype = 'uint8')
			mask = cv2.inRange(img_rgb, lower, upper)
			cv2.imwrite('mask_' + filename, mask)

# Blue 
analyze('bluemask', [120, 30, 20], [180, 90, 80])
#output([120, 30, 20], [180, 90, 80])
# Red
analyze('redmask', [25, 30, 175], [85, 90, 230])
#output([25, 30, 175], [85, 90, 230])
# Black
analyze('blackmask', [0, 0, 0], [45, 45, 45])
#output([0, 0, 0], [45, 45, 45])

''' Blue symbols: 51, 60, 148
Red symbols: 197, 57, 54
Green symbols: 31, 168, 79
Orange: 239, 130, 90'''