import sys
import os

import cv2

sys.path.append(os.path.abspath("../utils"))
from pcv_utils import load_pcv, gaussian_blur, mask, \
    roi_objects, analyze_objects, pseudolandmarks


def save_image(img, filename, suffix):
    os.makedirs("../transformed_images", exist_ok=True)
    filename = os.path.join('../transformed_images',
                            f"{filename}_{suffix}.JPG")
    cv2.imwrite(os.path.join("../transformed_images", filename), img)


def gen_transformed_images(img, filename: str):
    gaussian = gaussian_blur(img)
    masked = mask(img, gaussian)
    roi, roi_mask = roi_objects(img, masked)
    analyzed = analyze_objects(img, roi_mask)
    plm = pseudolandmarks(img, roi_mask)
    save_image(gaussian, filename, "gauss_blur")
    save_image(masked, filename, "mask")
    save_image(roi, filename, "roi")
    save_image(analyzed, filename, "analyze")
    save_image(plm, filename, "plm")


def main():
    try:
        if len(sys.argv) != 2:
            raise AssertionError("number of args must be 1")

        path = sys.argv[1]
        img = load_pcv(path)
        gen_transformed_images(img, os.path.basename(path))

    except Exception as e:
        print(f"{Exception.__name__}: {e}")


if __name__ == "__main__":
    main()
