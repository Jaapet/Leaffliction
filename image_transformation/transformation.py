import sys
import os
import argparse
import cv2

sys.path.append(os.path.abspath(".."))
import utils as utils

RESULTS_DIRECTORY="../transformed_images"


def save_image(img, filename, suffix, destination):
    os.makedirs(destination, exist_ok=True)
    filename_no_ext, _ = os.path.splitext(filename)
    new_filename = f"{filename_no_ext}_{suffix}.JPG"
    cv2.imwrite(os.path.join(destination, new_filename), img)


def gen_transformed_images(img, filename: str, destination: str):
    gaussian = utils.gaussian_blur(img)
    masked = utils.mask(img, gaussian)
    roi, roi_mask = utils.roi_objects(img, masked)
    analyzed = utils.analyze_objects(img, roi_mask)
    plm = utils.pseudolandmarks(img, roi_mask)
    save_image(gaussian, filename, "gauss_blur", destination)
    save_image(masked, filename, "mask", destination)
    save_image(roi, filename, "roi", destination)
    save_image(analyzed, filename, "analyze", destination)
    save_image(plm, filename, "plm", destination)


def transformation(args):
    source_path = args.source_explicit or args.source
    if not source_path:
        print("Error: You must provide a source path either as a positional argument or using -src.")
        sys.exit(1)

    destination_path = args.destination
    path_type = utils.path_type(source_path)

    if path_type:
        utils.check_directory(source_path)
        if utils.check_single_directory(source_path) == False:
            raise Exception("Given directory should not contain sub-directories.")
        files = utils.fetch_files(source_path)
        for file in files:
            img = utils.load_pcv(file)
            gen_transformed_images(img, os.path.basename(file), destination_path)
            print(f"\rtransformation.py: Augmentations for '{file}' done.\033[K", end="")
    else:
        utils.check_file(source_path)
        img = utils.load_pcv(source_path)
        gen_transformed_images(img, os.path.basename(source_path), destination_path)
        print(f"transformation.py: Augmentations for '{source_path}' done.")
    print(f"Transformations saved at '{destination_path}'.")

def main():
    try:
        parser = argparse.ArgumentParser(
            prog="Transformation",
            description="Creates multiple transformations of a given image or set of images."
        )
        parser.add_argument("source", nargs="?", default=None,
            help="Path to a single image or a directory of images."
        )
        parser.add_argument("-src", "--source_explicit", type=str,
            help="Explicit source path to an image or directory."
        )
        parser.add_argument("-dst", "--destination", type=str, default=RESULTS_DIRECTORY,
            help="Directory where transformed images will be saved (default: ../transformed_images)."
        )
        transformation(parser.parse_args())
    except Exception as e:
        print(f"transformation.py: {e}")


if __name__ == "__main__":
    main()
