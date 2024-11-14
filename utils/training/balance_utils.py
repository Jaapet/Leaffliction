import os
import utils as utils

DATASET_PATH = "./../images_dataset"


def save_dataset_image(group, img, filename, suffix, max):
    """
    Saves an augmented version of an image
    to the dataset directory if the maximum number
    of images for the group has not been reached.

    Parameters:
    - group (str): The group or category the image belongs to.
    - img (Image): The image object to save.
    - filename (str): Base name of the image file.
    - suffix (str): A suffix describing the augmentation type.
    - max (int): Maximum number of images allowed per group.

    Returns:
    - bool: False if the maximum number of images is reached,
            True otherwise.
    """
    os.makedirs(DATASET_PATH, exist_ok=True)
    sub_dataset_path = f"{DATASET_PATH}/{group}"
    if not os.path.exists(sub_dataset_path):
        os.makedirs(sub_dataset_path, exist_ok=True)
    entries = os.listdir(sub_dataset_path)
    if len(entries) >= max:
        print(f"\rtrain.py: Augmentations done for '{group}'\033[K")
        return False
    new_filename = f"{filename}_{suffix}.JPG"
    filename = os.path.join(sub_dataset_path, new_filename)
    img.save(filename, "JPEG")
    print(f"\rtrain.py: Augmentating image '{new_filename}' "
          "saved to {DATASET_PATH}\033[K", end="")
    return True


def transform_dataset_image(group, path, max):
    """
    Applies a series of transformations to an image and saves each one until
    the max image count for the group is reached.

    Parameters:
    - group (str): The group or category the image belongs to.
    - path (str): The file path to the original image.
    - max (int): Maximum number of images allowed per group.

    Returns:
    - bool: False if the maximum number of images is reached during processing,
            True otherwise.
    """
    filename = path.split('/')[-1].split('.')[0]
    img = utils.load_image(path)

    if not save_dataset_image(group, img, filename,
                              "original", max):
        return False
    if not save_dataset_image(group, utils.flip_image(img),
                              filename, "flip", max):
        return False
    if not save_dataset_image(group, utils.rotate_image(img),
                              filename, "rotate", max):
        return False
    if not save_dataset_image(group, utils.shear_image(img),
                              filename, "shear", max):
        return False
    if not save_dataset_image(group, utils.crop_image(img),
                              filename, "crop", max):
        return False
    if not save_dataset_image(group, utils.blur_image(img),
                              filename, "blur", max):
        return False
    if not save_dataset_image(group, utils.contrast_image(img),
                              filename, "contrast", max):
        return False
    return True


def upsample_dataset(images):
    """
    Balances dataset by applying transformations
    to images in each group to reach the maximum count
    of images in the largest group.

    Parameters:
    - images (dict): Dictionary mapping group names
                     to lists of image file paths.

    Returns:
    - None
    """
    max_images = max(len(value) for value in images.values())
    for group, images in images.items():
        for image in images:
            if not transform_dataset_image(group, image, max_images):
                break


def balance_dataset(directory):
    """
    Balances the dataset by upsampling each group
    to have an equal number of images.

    This function checks the dataset directory, fetches the images,
    groups them by category, and applies transformations to achieve balance.

    Parameters:
    - directory (str): Path to the directory containing the dataset images.

    Returns:
    - None
    """
    utils.check_directory(directory)
    images = utils.fetch_files(directory)
    grouped_images = utils.group_files(directory, images, True)
    upsample_dataset(grouped_images)
    print("train.py: Balancing dataset done.")
