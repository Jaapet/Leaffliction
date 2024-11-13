import os
import sys
import shutil
import argparse


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, \
    Flatten, Dense, Dropout, Input


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils


DATASET_PATH = "./../images_dataset"
MODEL_NAME = "trained_model.keras"


def train():
    """
    Trains a convolutional neural network (CNN)
    on the image dataset with data augmentation.

    Uses `ImageDataGenerator` to preprocess the images and performs training
    with a specified architecture of convolutional layers, dense layers,
    and dropout. Saves the trained model to a file specified by MODEL_NAME.

    Returns:
        None
    """
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    validation_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        '../images_dataset/train',
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical'
    )

    validation_generator = validation_datagen.flow_from_directory(
        '../images_dataset/val',
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical'
    )

    model = Sequential([
        Input(shape=(128, 128, 3)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(len(train_generator.class_indices), activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(
        train_generator,
        epochs=20,
        validation_data=validation_generator,
        verbose=1
    )

    model.save(MODEL_NAME)


def promt_reloading_tm(max_retries=2):
    """
    Prompts the user to confirm retraining
    the model if it already exists.
    """
    attempts = 0
    while attempts < max_retries:
        user_input = input(f"train.py: The trained model '{MODEL_NAME}' "
                           "already exists.\n"
                           "train.py: Do you want to retrain the model? "
                           "(yes/no): ").strip().lower()
        if user_input in {"yes", "y"}:
            return True
        elif user_input in {"no", "n"}:
            print("train.py: Retraining canceled.")
            return False
        else:
            print("Error: Invalid input. Please enter 'yes' or 'no'.")
            attempts += 1
    print("train.py: Too many invalid attempts. Retraining canceled.")
    return False


def train_model():
    """
    Manages model training, including confirmation prompts, existing model
    deletion, and error handling.

    Checks if a model file already exists, prompting the user for confirmation
    before overwriting. Deletes the existing model if confirmed and calls
    `train()` to perform the training.

    Returns:
        None
    """
    if os.path.exists(MODEL_NAME) and not promt_reloading_tm():
        return

    try:
        if os.path.exists(MODEL_NAME):
            os.remove(MODEL_NAME)
            print("train.py: Deleting previous trained model")
        train()
        print("train.py: Model training completed. " +
              f"Trained model saved as '{MODEL_NAME}'")

    except Exception as e:
        print(f"train.py: Error occurred while training model: {str(e)}")


def promt_reloading_ds(max_retries=2):
    """
    Prompts the user to confirm reloading
    the dataset if it already exists.
    """
    attempts = 0
    while attempts < max_retries:
        user_input = input(f"train.py: The dataset path '{DATASET_PATH}' "
                           "already exists.\n"
                           "train.py: Do you want to reload the dataset? "
                           "(yes/no): ").strip().lower()
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
    if os.path.exists(DATASET_PATH) and not promt_reloading_ds():
        return

    try:
        if os.path.exists(DATASET_PATH):
            shutil.rmtree(DATASET_PATH)
            print("train.py: Deleting previous dataset")
        utils.check_directory(directory)
        utils.balance_dataset(directory)
        utils.split_dataset()
        print("train.py: Loading dataset completed. " +
              f"Data saved at '{DATASET_PATH}'")

    except Exception as e:
        print(f"train.py: Error occurred while loading the dataset: {str(e)}")


def main(directory):
    """
    Main function to extract and analyze the
    dataset from images and generate charts.
    """
    load_dataset(directory)
    train_model()


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
