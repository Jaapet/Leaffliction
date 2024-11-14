from plantcv import plantcv as pcv
import cv2
import rembg


def load_pcv(path: str):
    """
    Loads an image using OpenCV.

    Parameters:
    - path (str): Path to the image file.

    Returns:
    - numpy.ndarray: The loaded image as a NumPy array.
    """
    img = cv2.imread(path)
    return img


def gaussian_blur(img):
    """
    Applies Gaussian blur to an image after removing its
    background and applying a binary threshold.

    Parameters:
    - img (numpy.ndarray): The input image to blur.

    Returns:
    - numpy.ndarray: The thresholded and blurred image.
    """
    img = rembg.remove(img)
    gray = pcv.rgb2gray_lab(rgb_img=img,
                            channel='l')
    tresholded = pcv.threshold.binary(gray_img=gray,
                                      threshold=35,
                                      object_type='light')
    return pcv.gaussian_blur(img=tresholded,
                             ksize=(5, 5),
                             sigma_x=0,
                             sigma_y=None)


def mask(img, mask):
    """
    Applies a mask to an image, setting masked regions to white.

    Parameters:
    - img (numpy.ndarray): The input image to mask.
    - mask (numpy.ndarray): The binary mask to apply.

    Returns:
    - numpy.ndarray: The masked image.
    """
    return pcv.apply_mask(img=img,
                          mask=mask,
                          mask_color='white')


def roi_objects(img, mask):
    """
    Creates a region of interest (ROI) mask on the input
    image and highlights the ROI on the original image.

    Parameters:
    - img (numpy.ndarray): The original image.
    - mask (numpy.ndarray): The binary mask defining the object regions.

    Returns:
    - tuple: A tuple with:
        - (numpy.ndarray): The image with ROI highlighted.
        - (numpy.ndarray): The ROI mask.
    """
    roi = pcv.roi.rectangle(img=mask,
                            x=0,
                            y=0,
                            w=img.shape[0],
                            h=img.shape[1])
    roi_mask = pcv.roi.filter(mask=pcv.threshold.binary(
                              gray_img=pcv.rgb2gray_lab(
                                rgb_img=rembg.remove(img),
                                channel='l'),
                              threshold=35,
                              object_type='light'),
                              roi=roi,
                              roi_type='partial')
    cpy = img.copy()
    cpy[(roi_mask != 0), 0] = 0
    cpy[(roi_mask != 0), 1] = 255
    cpy[(roi_mask != 0), 2] = 0
    return cpy, roi_mask


def analyze_objects(img, mask):
    """
    Analyzes the size and shape of objects within a masked region.

    Parameters:
    - img (numpy.ndarray): The original image.
    - mask (numpy.ndarray): The labeled mask of object regions.

    Returns:
    - dict: A dictionary containing size analysis results.
    """
    return pcv.analyze.size(img=img,
                            labeled_mask=mask)


def pseudolandmarks(img, mask):
    """
    Adds pseudolandmark points to the input image, marking key areas.

    Parameters:
    - img (numpy.ndarray): The original image.
    - mask (numpy.ndarray): The mask to define landmark locations.

    Returns:
    - numpy.ndarray: The image with pseudolandmarks added.
    """
    top, bot, center_v = pcv.homology.x_axis_pseudolandmarks(img=img,
                                                             mask=mask,
                                                             label='default')
    img = draw_pseudolandmarks(img, top, (0, 0, 255), 5)
    img = draw_pseudolandmarks(img, bot, (255, 0, 255), 5)
    img = draw_pseudolandmarks(img, center_v, (255, 0, 0), 5)
    return img


def draw_pseudolandmarks(img, plms, color, radius):
    """
    Draws pseudolandmarks as colored circles on the image
    at specified points.

    Parameters:
    - img (numpy.ndarray): The image on which to draw.
    - plms (list): List of pseudolandmark coordinates.
    - color (tuple): Color of the circles as an (R, G, B) tuple.
    - radius (int): Radius of the landmark circles.

    Returns:
    - numpy.ndarray: The image with pseudolandmarks drawn.
    """
    for i in range(len(plms)):
        if len(plms[i]) >= 1 and len(plms[i][0]) >= 2:
            center_x = plms[i][0][1]
            center_y = plms[i][0][0]
            for x in range(img.shape[0]):
                for y in range(img.shape[1]):
                    if (x - center_x) ** 2 + (y - center_y) ** 2 <=\
                            radius ** 2:
                        img[x, y] = color
    return img
