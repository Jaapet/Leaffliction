import os
import sys
import random
import shutil
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils

DATASET_PATH = "./../images_dataset"

def promt_reloading(max_retries=2):
    """Prompts the user to confirm reloading the dataset if it already exists."""
    attempts = 0
    while attempts < max_retries:
        user_input = input(f"train.py: The dataset path '{DATASET_PATH}' already exists.\n"
                           "train.py: Do you want to reload the dataset? (yes/no): ").strip().lower()
        if user_input in {"yes", "y"}:
            return True
        elif user_input in {"no", "n"}:
            print("train.py: Reloading canceled.")
            return False
        else:
            print("Error: Invalid input. Please enter 'yes' or 'no'.")
            attempts += 1
    print("train.py: Too many invalid attempts. Reloading canceled.")
    return False


def load_dataset(directory):
    """Main function to load, balance, and split the dataset."""
    if os.path.exists(DATASET_PATH) and not promt_reloading():
        return

    try:
        if os.path.exists(DATASET_PATH):
            shutil.rmtree(DATASET_PATH)
            print("train.py: Deleting previous dataset")
        utils.check_directory(directory)
        utils.balance_dataset(directory)
        utils.split_dataset()
        print(f"train.py: Loading dataset completed. Data saved at '{DATASET_PATH}'")

    except Exception as e:
        print(f"train.py: Error occurred while loading the dataset: {str(e)}")


def main(directory):
    """Main function to extract and analyze the dataset from images and generate charts."""
    load_dataset(directory)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="Train",
            description="Train a model using a dataset of images"
        )
        parser.add_argument("images_directory", type=str,
                            help="Path to the images directory")
        args = parser.parse_args()
        main(args.images_directory)

    except Exception as e:
        print(f"train.py: error: {e}")