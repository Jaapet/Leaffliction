import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model


MODEL_PATH = 'trained_model.keras'
TEST_DATASET_PATH = '../images_dataset/test'


def evaluate():
    """
    Loads a trained model and evaluates
    its performance on a test dataset.

    This function:
    - Loads the pre-trained model from MODEL_PATH.
    - Prepares the test dataset using ImageDataGenerator with rescaling.
    - Uses the model to evaluate the test data,
      printing the accuracy and loss.

    Parameters:
    None

    Returns:
    None
    """
    model = load_model(MODEL_PATH)

    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_directory(
        TEST_DATASET_PATH,
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    loss, accuracy = model.evaluate(test_generator, verbose=1)
    print(f"Accuracy : {accuracy}  |  Loss : {loss}")


def main():
    """
    Main function to run the evaluation of the trained model.

    This function calls evaluate()
    to load the model and perform evaluation.

    Parameters:
    None

    Returns:
    None
    """
    evaluate()


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"evaluate.py: error: {e}")
