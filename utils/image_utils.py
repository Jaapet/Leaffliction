from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import random


def load_image(path: str) -> Image:
    """
    Loads an image from a specified file path, converts it to RGB,
    and prints its shape and content.

    Parameters:
    - path (str): The file path to the image.

    Returns:
    - Image: The loaded image in PIL format.

    Raises:
    - Exception: If the image cannot be loaded.
    """
    try:
        img = Image.open(path)
        return img
    except Exception as e:
        print(f"{Exception.__name__}: {e}")
        print("Failed to load the image")
        exit()


def flip_image(img: Image):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def rotate_image(img, angle=10):
    return img.rotate(angle)


def shear_image(img, shear_factor=0.2):
    return img.transform(img.size, Image.AFFINE,
                         (1, shear_factor, 0, 0, 1, 0), Image.BICUBIC)


def crop_image(img, crop_fraction=0.8):
    width, height = img.size
    new_width = int(width * crop_fraction)
    new_height = int(height * crop_fraction)
    left = random.randint(0, width - new_width)
    top = random.randint(0, height - new_height)
    return img.crop((left, top, left + new_width, top + new_height))


def blur_image(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def contrast_image(img, factor=2):
    return ImageEnhance.Contrast(img).enhance(factor)
