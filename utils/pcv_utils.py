from plantcv import plantcv as pcv
import cv2
import rembg
import numpy as np
import os

def load_pcv(path: str):
	img = cv2.imread(path)
	return img

def gaussian_blur(img):
	img = rembg.remove(img)
	gray = pcv.rgb2gray_lab(rgb_img=img, channel='l')
	tresholded = pcv.threshold.binary(gray_img=gray, threshold=35, object_type='light')
	return pcv.gaussian_blur(img=tresholded, ksize=(5, 5), sigma_x=0, sigma_y=None)

def mask(img):
	# hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# mask = pcv.threshold.binary(hsv_img, threshold=120, max_value=255, object_type='light')
	return pcv.apply_mask(img=img, mask=gaussian_blur(img), mask_color='white')

# def roi_objects(img):


# def analyze_objects(img):


# def pseudolandmarks(img):
