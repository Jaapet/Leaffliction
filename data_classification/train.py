import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils

DATASET_PATH = "./../images_dataset"

# def split_dataset():
#     files = utils.fetch_files(DATASET_PATH)
#     grouped_files = utils.group_files(DATASET_PATH, files)
#     for file in grouped_files:
#         print("->", file)
#     return

def main(directory):
    """
    Main function to extract and analyze the dataset from images
    and generate charts.

    Parameters:
        directory (str): The directory path.
    Returns: None
    Raises: None
    """

    utils.check_directory(directory)
    files = utils.fetch_files(directory)
    utils.balance_dataset(directory)
    # split_dataset()

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
