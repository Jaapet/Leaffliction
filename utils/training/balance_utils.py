import os
import shutil
import utils as utils

DATASET_PATH = "./../images_dataset"


def save_dataset_image(group, img, filename, suffix, max):
    os.makedirs(DATASET_PATH, exist_ok=True)
    sub_dataset_path = f"{DATASET_PATH}/{group}"
    if not os.path.exists(sub_dataset_path):
        os.makedirs(sub_dataset_path, exist_ok=True)
    entries = os.listdir(sub_dataset_path)
    if len(entries) >= max:
        print(f"\rtrain.py: Augmentations done for {group}\033[K")
        return False
    new_filename = f"{filename}_{suffix}.JPG"
    filename = os.path.join(sub_dataset_path, new_filename)
    img.save(filename, "JPEG")
    print(f"\rtrain.py: Augmentating image {new_filename} "
          "saved to {DATASET_PATH}\033[K", end="")
    return True


def transform_dataset_image(group, path, max):
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

    if os.path.exists(DATASET_PATH):
        shutil.rmtree(DATASET_PATH)
        print("train.py: Deleting previous dataset")
    max_images = max(len(value) for value in images.values())
    for group, images in images.items():
        for image in images:
            if not transform_dataset_image(group, image, max_images):
                break


def balance_dataset(directory, max_retries=2):
    utils.check_directory(directory)

    if os.path.exists(DATASET_PATH):
        attempts = 0
        while attempts < max_retries:
            try:
                user_input = input(f"train.py: The dataset path "
                                   f"'{DATASET_PATH}' already exists.\n"
                                   "train.py: Do you want to "
                                   "rebalance the dataset? (yes/no): "
                                   ).strip().lower()

                if user_input in {"yes", "y"}:
                    break
                elif user_input in {"no", "n"}:
                    print("train.py: Rebalancing canceled.")
                    return
                else:
                    raise ValueError("Invalid input. Please enter "
                                     "'yes' or 'no'.")

            except ValueError as ve:
                print(f"Error: {ve}")
                attempts += 1

            except (KeyboardInterrupt, EOFError):
                print("\ntrain.py: Operation interrupted by user. "
                      "Rebalacing canceled.")
                return

        if attempts >= max_retries:
            print("train.py: Too many invalid attempts. "
                  "Rebalancing canceled.")
            return
    try:
        images = utils.fetch_files(directory)
        grouped_images = utils.group_files(directory, images, True)
        upsample_dataset(grouped_images)
        print(f"train.py: Balancing dataset done. Saved at {DATASET_PATH}")

    except Exception as e:
        print(f"train.py: An error occurred while balancing the dataset: "
              f"{str(e)}")
