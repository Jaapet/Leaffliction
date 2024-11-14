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
    """
    Flips the image horizontally (left to right).

    Parameters:
    - img (Image): The input image to flip.

    Returns:
    - Image: The horizontally flipped image.
    """
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def rotate_image(img, angle=10):
    """
    Rotates the image by a specified angle.

    Parameters:
    - img (Image): The input image to rotate.
    - angle (int, optional): The angle in degrees to rotate the image.

    Returns:
    - Image: The rotated image.
    """
    return img.rotate(angle)


def shear_image(img, shear_factor=0.2):
    """
    Applies a shearing transformation to the image.

    Parameters:
    - img (Image): The input image to shear.
    - shear_factor (float, optional): The factor by which to shear the image.
      Defaults to 0.2.

    Returns:
    - Image: The sheared image.
    """
    return img.transform(img.size, Image.AFFINE,
                         (1, shear_factor, 0, 0, 1, 0), Image.BICUBIC)


def crop_image(img, crop_fraction=0.8):
    """
    Randomly crops a portion of the image.

    Parameters:
    - img (Image): The input image to crop.
    - crop_fraction (float, optional): Fraction of the image
                                       dimensions to retain after
                                       cropping. Defaults to 0.8 (80%).

    Returns:
    - Image: The cropped image.
    """
    width, height = img.size
    new_width = int(width * crop_fraction)
    new_height = int(height * crop_fraction)
    left = random.randint(0, width - new_width)
    top = random.randint(0, height - new_height)
    return img.crop((left, top, left + new_width, top + new_height))


def blur_image(img, radius=2):
    """
    Applies a Gaussian blur to the image.

    Parameters:
    - img (Image): The input image to blur.
    - radius (int, optional): The blur radius.
      Higher values produce more blur. Defaults to 2.

    Returns:
    - Image: The blurred image.
    """
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def contrast_image(img, factor=2):
    """
    Enhances the contrast of the image.

    Parameters:
    - img (Image): The input image to adjust contrast.
    - factor (float, optional): The factor by which to increase the contrast.
      A factor greater than 1 increases contrast; less than 1 decreases it.
      Defaults to 2.

    Returns:
    - Image: The contrast-enhanced image.
    """
    return ImageEnhance.Contrast(img).enhance(factor)
