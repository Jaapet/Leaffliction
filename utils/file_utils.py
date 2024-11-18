import os


def check_directory(directory):
    """
    Check if the directory exists, is readable, and has files.

    Parameters:
        directory (str): The directory to check.
    Returns: None
    Raises:
        Exception: If the directory does not exist.
        Exception: If the directory is not readable.
        Exception: If the directory is empty.
    """
    if not os.path.exists(directory):
        raise Exception(f"Directory does not exist: {directory}")
    if not os.path.isdir(directory):
        raise Exception(f"Path is not a directory: {directory}")
    if not os.access(directory, os.R_OK):
        raise Exception(f"Directory is not readable: {directory}")
    if not os.listdir(directory):  # Check if the directory is empty
        raise Exception(f"Directory is empty: {directory}")

def check_single_directory(directory):
    """
    Checks if a given directory contains only files and no subdirectories.

    Parameters:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory contains only files, False otherwise.

    Raises:
        Exception: If the provided path is not a directory or does not exist.
    """
    if not os.path.exists(directory):
        raise Exception(f"Directory does not exist: {directory}")
    if not os.path.isdir(directory):
        raise Exception(f"Path is not a directory: {directory}")
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            return False
    
    return True


def check_file(file_path):
    """
    Check if the file exists and is readable.

    Parameters:
        file_path (str): The file to check.
    Returns: None
    Raises:
        Exception: If the file does not exist.
        Exception: If the file is not readable.
    """
    if not os.path.exists(file_path):
        raise Exception(f"File does not exist: {file_path}")
    if not os.access(file_path, os.R_OK):
        raise Exception(f"File is not readable: {file_path}")
    if os.path.isdir(file_path):
        raise Exception(f"Path is a directory, not a file: {file_path}")

def fetch_files(directory):
    """
    Walk through the directory and its subdirectories to
    get all image files.

    Parameters:
        directory (str): The directory to walk through.
    Returns:
        files (list): A list of all image files in the directory.
    Raises:
        Exception: If the file format is not supported.
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if not filename.lower().endswith(('.png', '.jpg',
                                              '.jpeg', '.bmp', '.gif')):
                raise Exception(f"Unsupported file format: {filename}")
            files.append(os.path.join(root, filename))
    return files


def group_files(directory, files, absolute=False):
    """
    Group files by their last-level subfolder.

    Parameters:
        directory (str): The directory name.
        files (list): A list of all image files in the directory.
        absolute (bool): If True, the list of files will be
            returned as absolraise Exceptionute paths.
    Returns:
        content (dict): A dictionary with the last-level
            subfolder as keys and the number of files as values.
    Raises: None
    """
    content = {}

    for file_path in files:
        relative_path = os.path.relpath(file_path, directory)
        parts = relative_path.split(os.sep)
        if len(parts) > 1:
            last_subfolder = parts[-2]
            if last_subfolder not in content:
                content[last_subfolder] = []
            if absolute:
                content[last_subfolder].append(file_path)
            else:
                content[last_subfolder].append(parts[-1])
    return content

def path_type(path):
    """
    Check if the path is a directory or a file.

    Parameters:
        path (str): The path to check.

    Returns:
        bool: True if it's a directory, False if it's a file. None if it doesn't exist.
    """
    if not os.path.exists(path):
        raise Exception(f"Path does not exist: {path}")
    return os.path.isdir(path)