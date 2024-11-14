import sys
import os

import cv2

sys.path.append(os.path.abspath(".."))
import utils as utils


def save_image(img, filename, suffix):
    """
    Saves a transformed image with a specified suffix
    in the '../transformed_images' directory.

    Parameters:
    img (numpy.ndarray): The transformed image to save.
    filename (str): The base name of the file without any suffix.
    suffix (str): The suffix describing the transformation type.

    Returns:
    None
    """
    os.makedirs("../transformed_images", exist_ok=True)
    filename = os.path.join('../transformed_images',
                            f"{filename}_{suffix}.JPG")
    cv2.imwrite(os.path.join("../transformed_images", filename), img)


def gen_transformed_images(img, filename: str):
    """
    Generates multiple transformed versions of
    an input image (Gaussian blurred, masked, ROI,
    analyzed, and pseudolandmarked) and saves
    each one with a specific suffix to indicate
    the transformation type.

    Parameters:
    img (numpy.ndarray): The original image to be transformed.
    filename (str): The base name of the image file,
    used as a prefix for the saved transformed images.

    Returns:
    None
    """
    gaussian = utils.gaussian_blur(img)
    masked = utils.mask(img, gaussian)
    roi, roi_mask = utils.roi_objects(img, masked)
    analyzed = utils.analyze_objects(img, roi_mask)
    plm = utils.pseudolandmarks(img, roi_mask)
    save_image(gaussian, filename, "gauss_blur")
    save_image(masked, filename, "mask")
    save_image(roi, filename, "roi")
    save_image(analyzed, filename, "analyze")
    save_image(plm, filename, "plm")


def main():
    """
    Main function to load an image from the specified path
    and generate multiple transformed versions.

    This function:
    - Verifies the correct number of arguments is passed (expects 1 argument).
    - Loads the specified image using utils.load_pcv().
    - Calls gen_transformed_images() to create and save the transformed images.

    Raises:
    AssertionError: If the incorrect number of arguments is provided.
    Exception: For general errors during image loading or transformation.

    Returns:
    None
    """
    try:
        if len(sys.argv) != 2:
            raise AssertionError("number of args must be 1")

        path = sys.argv[1]
        img = utils.load_pcv(path)
        gen_transformed_images(img, os.path.basename(path))

    except Exception as e:
        print(f"{Exception.__name__}: {e}")


if __name__ == "__main__":
    main()
