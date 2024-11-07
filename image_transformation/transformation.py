import sys
import os

from plantcv import plantcv as pcv
import cv2

sys.path.append(os.path.abspath("../utils"))
from image_utils import *
from pcv_utils import *


def save_image(img, filename, suffix):
	os.makedirs("../transformed_images", exist_ok=True)
	filename = os.path.join('../transformed_images', f"{filename}_{suffix}.JPG")
	cv2.imwrite(os.path.join("../transformed_images", filename), img)


def	gen_transformed_images(img, filename: str):
	gaussian = gaussian_blur(img)
	masked = mask(img, gaussian)
	roi = roi_objects(img, masked)
	save_image(gaussian, filename, "gauss_blur")
	save_image(masked, filename, "mask")
	save_image(roi, filename, "roi")
	# save_image(analyze_ojects(img), filename, "analyze")
	# save_image(pseudolandmarks(img), filename, "plm")


def main():
	# try:
		
		if len(sys.argv) != 2:
			raise AssertionError("number of args must be 1")

		path = sys.argv[1]
		img = load_pcv(path)
		gen_transformed_images(img, os.path.basename(path))

	# except Exception as e:
	# 	print(f"{Exception.__name__}: {e}")


if __name__ == "__main__":
	main()