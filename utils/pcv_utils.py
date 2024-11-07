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

def mask(img, mask):
	return pcv.apply_mask(img=img, mask=mask, mask_color='white')

def roi_objects(img, mask):
	roi = pcv.roi.rectangle(img=mask, x=0, y=0, w=img.shape[0], h=img.shape[1])
	roi_mask = pcv.roi.filter(mask=pcv.threshold.binary(gray_img=pcv.rgb2gray_lab(rgb_img=rembg.remove(img), channel='l'), threshold=35, object_type='light'), roi=roi, roi_type='partial')
	cpy = img.copy()
	cpy[(roi_mask != 0), 0] = 0
	cpy[(roi_mask != 0), 1] = 255
	cpy[(roi_mask != 0), 2] = 0
	return cpy

# def analyze_objects(img):


# def pseudolandmarks(img):
