import sys
import os
from image_utils import *


def save_image(img, filename, suffix):
	os.makedirs("augmented_images", exist_ok=True)
	filename = os.path.join('augmented_images', f"{filename}_{suffix}.JPG")
	img.save(filename, "JPEG")


def	gen_augmented_images(img: Image, filename: str):
	save_image(flip_image(img), filename, "flip")
	save_image(rotate_image(img), filename, "rotate")
	save_image(shear_image(img), filename, "shear")
	save_image(crop_image(img), filename, "crop")
	save_image(blur_image(img), filename, "blur")
	save_image(contrast_image(img), filename, "contrast")


def main():
	try:
		
		if len(sys.argv) != 2:
			raise AssertionError("number of args must be 1")

		path = sys.argv[1]
		img = load_image(path)
		gen_augmented_images(img, os.path.basename(path))

	except Exception as e:
		print(f"{Exception.__name__}: {e}")


if __name__ == "__main__":
	main()