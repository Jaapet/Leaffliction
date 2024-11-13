import argparse
import os
import sys
import numpy as np


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils


MODEL_PATH = 'trained_model.keras'


class_indices = {
    0: 'Apple_Black_rot',
    1: 'Apple_Healthy',
    2: 'Apple_Rust',
    3: 'Apple_Scab',
    4: 'Grape_Black_rot',
    5: 'Grape_Esca',
    6: 'Grape_Healthy',
    7: 'Grape_Spot'
}


def load_and_predict(img_path):
    """
    Loads a trained model and predicts the class of a given image.

    Preprocesses the image by resizing it, converting it to a numpy array,
    expanding dimensions to simulate a batch, and normalizing pixel values.
    Then, it uses the loaded model to make a prediction on the image.

    Args:
        img_path (str): The file path to the image to be classified.

    Returns:
        None: Prints the predicted class name for the image.
    """

    model = load_model(MODEL_PATH)

    # Redimensionner l'image à 128x128
    img = image.load_img(img_path, target_size=(128, 128))
    # Convertir l'image en array numpy
    img_array = img_to_array(img)
    # Ajouter une dimension pour simuler un batch
    img_array = np.expand_dims(img_array, axis=0)
    # Normaliser les pixels entre 0 et 1
    img_array = img_array / 255.0

    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction, axis=1)

    predicted_class_name = class_indices[predicted_class[0]]
    print(f"Image class: {predicted_class_name}")


def main(image):
    """
    Main function to validate the image path and perform the prediction.

    Checks that the specified image file exists using a utility function.
    Then, calls `load_and_predict()` to classify the image.

    Args:
        image (str): The file path to the image to be classified.

    Returns:
        None
    """

    utils.check_file(image)
    load_and_predict(image)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="Predict",
            description="Predicts the class of an image "
            "using a previously trained model"
        )
        parser.add_argument("image", type=str,
                            help="Path to an image to predict")
        args = parser.parse_args()
        main(args.image)

    except Exception as e:
        print(f"predict.py: error: {e}")
