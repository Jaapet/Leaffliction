import sys
import os
import argparse

sys.path.append(os.path.abspath(".."))
import utils as utils

RESULTS_DIRECTORY="../augmented_directory"

def save_image(img, filename, suffix):
    """
    Saves an augmented image with a specific suffix
    in the '../augmented_directory' directory.

    Parameters:
    img (PIL.Image): The augmented image to be saved.
    filename (str): The base name of the file without any suffix.
    suffix (str): The suffix describing the augmentation type.

    Returns:
    None
    """
    os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
    filename = os.path.join(RESULTS_DIRECTORY, f"{filename}_{suffix}.JPG")
    img.save(filename, "JPEG")


def gen_augmented_images(img, filename: str):
    """
    Generates multiple augmented images
    (flipped, rotated, sheared, cropped, blurred, contrast-adjusted)
    and saves each one with a specific suffix
    to distinguish the augmentation type.

    Parameters:
    img (PIL.Image): The original image to be augmented.
    filename (str): The base name of the image file,
    used as a prefix for the saved augmented images.

    Returns:
    None
    """
    save_image(img, filename, "original")
    save_image(utils.flip_image(img), filename, "flip")
    save_image(utils.rotate_image(img), filename, "rotate")
    save_image(utils.shear_image(img), filename, "shear")
    save_image(utils.crop_image(img), filename, "crop")
    save_image(utils.blur_image(img), filename, "blur")
    save_image(utils.contrast_image(img), filename, "contrast")
    print(f"augmentation.py: Augmentations done. Save at '{RESULTS_DIRECTORY}'.")


def main():
    """
    Main function to load an image from the provided path
    and generate multiple augmented versions of it.

    This function:
    - Checks that the correct number of arguments is passed (expects 1).
    - Loads the specified image using utils.load_image().
    - Calls gen_augmented_images() to create and save the augmented images.

    Raises:
    AssertionError: If the incorrect number of arguments is provided.
    Exception: For general errors during image loading or augmentation.

    Returns:
    None
    """
    try:
        parser = argparse.ArgumentParser(
            prog="Augmentation",
            description="Creates 6 different augmentations of a \
                given image"
        )
        parser.add_argument("image_path", type=str,
                            help="Path to the an image")
        args = parser.parse_args()
        path = args.image_path
        utils.check_file(path)
        img = utils.load_image(path)
        gen_augmented_images(img, os.path.basename(path))

    except Exception as e:
        print(f"augmentation.py: {Exception.__name__}: {e}")


if __name__ == "__main__":
    main()
