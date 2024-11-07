import argparse
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils

# 1. Balance the dataset as ../images
# Grape_Esca: 2764
# Grape_healthy: 844
# Apple_scab: 1258
# Grape_Black_rot: 2356
# Apple_healthy: 3280
# Grape_spot: 2150
# Apple_rust: 550
# Apple_Black_rot: 1240
# => Add tranformations to the different classes to 
# reduce overfitting and improve the model's performance
# (supposedly done in the data augmentation script)

# 2. Train model using the dataset
# https://fastai1.fast.ai/vision.html



def balance(directory):

    utils.check_directory(directory)
    files = utils.fetch_files(directory)
    grouped_files = utils.group_files(directory, files)
    for key, value in grouped_files.items():
        print(f"{key}: {len(value)}")

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
    balance(directory)

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
