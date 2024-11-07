import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils


def main(image):
    """
    Main function to extract and analyze the dataset from images
    and generate charts.

    Parameters:
        image (str): The image path.
    Returns: None
    Raises: None
    """

    utils.check_file(image)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="Predict",
            description="Predict the class of an image using a previously trained model"
        )
        parser.add_argument("image", type=str,
                            help="Path to an image to predict")
        args = parser.parse_args()
        main(args.images_directory)

    except Exception as e:
        print(f"predict.py: error: {e}")
