import sys
import os

sys.path.append(os.path.abspath(".."))
import utils as utils


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
    os.makedirs("../augmented_directory", exist_ok=True)
    filename = os.path.join('../augmented_directory', f"{filename}_{suffix}.JPG")
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
    save_image(utils.flip_image(img), filename, "flip")
    save_image(utils.rotate_image(img), filename, "rotate")
    save_image(utils.shear_image(img), filename, "shear")
    save_image(utils.crop_image(img), filename, "crop")
    save_image(utils.blur_image(img), filename, "blur")
    save_image(utils.contrast_image(img), filename, "contrast")


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
        if len(sys.argv) != 2:
            raise AssertionError("number of args must be 1")

        path = sys.argv[1]
        img = utils.load_image(path)
        gen_augmented_images(img, os.path.basename(path))

    except Exception as e:
        print(f"{Exception.__name__}: {e}")


if __name__ == "__main__":
    main()
