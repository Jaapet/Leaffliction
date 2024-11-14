import os
import random
import shutil
import utils as utils

DATASET_PATH = "./../images_dataset"


def shuffle_dataset_image(images, split_ratios):
    """
    Shuffles and splits a list of image paths into training,
    validation, and test sets based on specified split ratios.

    Parameters:
    - images (list): List of file paths for images in a particular group.
    - split_ratios (dict): Dictionary with keys 'train', 'val', and 'test'
      indicating the ratio for each split.

    Returns:
    - dict: Dictionary with keys 'train', 'val', and 'test'
            each containing a list of image paths belonging to that split.
    """
    random.shuffle(images)
    train_idx = int(len(images) * split_ratios['train'])
    val_idx = train_idx + int(len(images) * split_ratios['val'])
    return {
        'train': images[:train_idx],
        'val': images[train_idx:val_idx],
        'test': images[val_idx:]
    }


def copy_dataset_image(splits, group, split_paths):
    """
    Copies images into separate directories for
    training, validation, and test sets.

    Parameters:
    - splits (dict): Dictionary with split keys mapping to lists
      of image file paths for each split.
    - group (str): The group or category the images belong to.
    - split_paths (dict): Dictionary mapping split keys to
      target directories for each split.

    Returns:
    - None
    """
    for split, split_images in splits.items():
        split_dir = os.path.join(split_paths[split], group)
        os.makedirs(split_dir, exist_ok=True)
        for image_path in split_images:
            shutil.copy(image_path, split_dir)


def split_dataset():
    """
    Splits the dataset into training, validation,
    and test directories based on predefined ratios.
    This function shuffles and copies images from each category
    into their respective split directories,
    removing the original directories afterwards.

    Parameters:
    - None

    Returns:
    - None
    """
    images = utils.fetch_files(DATASET_PATH)
    grouped_images = utils.group_files(DATASET_PATH, images, True)

    split_ratios = {'train': 0.7, 'val': 0.15, 'test': 0.15}
    split_paths = {
        'train': os.path.join(DATASET_PATH, 'train'),
        'val': os.path.join(DATASET_PATH, 'val'),
        'test': os.path.join(DATASET_PATH, 'test')
    }
    for path in split_paths.values():
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    for group, group_images in grouped_images.items():
        print(f"train.py: Splitting images for '{group}'...\033[K", end="")
        splits = shuffle_dataset_image(group_images, split_ratios)
        copy_dataset_image(splits, group, split_paths)

        original_group_dir = os.path.join(DATASET_PATH, group)
        if os.path.exists(original_group_dir):
            shutil.rmtree(original_group_dir)
        print(f"\rtrain.py: Splitting done for '{group}'...\033[K")
    print("train.py: Dataset splitting completed.\033[K")
