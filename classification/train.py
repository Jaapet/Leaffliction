import argparse
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath("../utils"))
from file_utils import *

def main(directory):
    """
    Main function to extract and analyze the dataset from images
    and generate charts.

    Parameters:
        directory (str): The directory path.
    Returns: None
    Raises: None
    """
    files = fetch_files(directory)
    grouped_files = group_files(directory, files)
    for key, value in grouped_files.items():
        print(f"{key}: {len(value)}")

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
        print(f"Distribution.py: error: {e}")
