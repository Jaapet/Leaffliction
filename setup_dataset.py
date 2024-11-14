import os
import shutil


def promt_reloading(max_retries=2):
    """
    Prompts the user to reload the dataset if it already exists.
    Allows a maximum number of attempts to provide a valid response.

    Parameters:
    - max_retries (int): Maximum number of attempts for user input.

    Returns:
    - bool: True if the user confirms reloading, False otherwise.
    """
    attempts = 0
    while attempts < max_retries:
        user_input = input("setup_dataset.py: The dataset path 'images' " +
                           "already exists.\n" +
                           "setup_dataset.py: " +
                           "Do you want to reload the dataset? " +
                           "(yes/no): ").strip().lower()
        if user_input in {"yes", "y"}:
            return True
        elif user_input in {"no", "n"}:
            print("setup_dataset.py: Reloading canceled.")
            return False
        else:
            print("Error: Invalid input. Please enter 'yes' or 'no'.")
            attempts += 1
    print("setup_dataset.py: Too many invalid attempts. Reloading canceled.")
    return False


def setup_dataset():
    """
    Sets up the dataset directory structure by organizing image files based on
    category names. If a previous dataset exists,
    it offers the option to reload it.

    The function organizes images by moving subdirectories with names starting
    with 'Apple' and 'Grape' into respective 'apples' and 'grapes' directories.

    Raises:
    - Exception: If an error occurs during the directory or file operations.
    """
    if not os.path.exists('leaves/images'):
        print("setup_dataset.py: 'leaves/images' doesn't exists")
        return

    if os.path.exists('images') and not promt_reloading():
        return

    try:
        if os.path.exists('images'):
            shutil.rmtree('images')
            print("setup_dataset.py: Deleting previous dataset")
        os.mkdir("images")
        os.mkdir("images/apples")
        os.mkdir("images/grapes")

        for subdir in os.listdir('leaves/images'):
            subdir_path = os.path.join('leaves/images', subdir)
            if os.path.isdir(subdir_path):
                if subdir.startswith("Apple"):
                    shutil.move(subdir_path, 'images/apples')
                elif subdir.startswith("Grape"):
                    shutil.move(subdir_path, 'images/grapes')
        shutil.rmtree('leaves')

        print("setup_dataset.py: Setup dataset completed. " +
              "Data saved at 'images'")

    except Exception as e:
        print("setup_dataset.py:" +
              f"Error occurred while setup the dataset: {str(e)}")


def main():
    """
    Entry point of the script that initializes the dataset setup.
    """
    setup_dataset()


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"setup_dataset.py: error: {e}")
