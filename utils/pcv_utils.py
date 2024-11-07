from plantcv import plantcv as pcv
import cv2
import rembg


def load_pcv(path: str):
    img = cv2.imread(path)
    return img


def gaussian_blur(img):
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
    return pcv.apply_mask(img=img,
                          mask=mask,
                          mask_color='white')


def roi_objects(img, mask):
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
    return pcv.analyze.size(img=img,
                            labeled_mask=mask)


def pseudolandmarks(img, mask):
    top, bot, center_v = pcv.homology.x_axis_pseudolandmarks(img=img,
                                                             mask=mask,
                                                             label='default')
    img = draw_pseudolandmarks(img, top, (0, 0, 255), 5)
    img = draw_pseudolandmarks(img, bot, (255, 0, 255), 5)
    img = draw_pseudolandmarks(img, center_v, (255, 0, 0), 5)
    return img


def draw_pseudolandmarks(img, plms, color, radius):
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
