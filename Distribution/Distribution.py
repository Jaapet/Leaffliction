import argparse
import os
import matplotlib.pyplot as plt

RESULTS_RELATIVE_PATH = "Distribution/Results"
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
if CURRENT_WORKING_DIRECTORY.split(os.sep)[-1] == "Distribution":
    RESULTS_DIRECTORY = f"{CURRENT_WORKING_DIRECTORY}/Results"
else:
    RESULTS_DIRECTORY = f"{CURRENT_WORKING_DIRECTORY}/{RESULTS_RELATIVE_PATH}"
PIE_CHART_FILENAME = "pie_chart.png"
BAR_CHART_FILENAME = "bar_chart.png"


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


def group_files(directory, files):
    """
    Group files by their last-level subfolder.

    Parameters:
        directory (str): The directory name.
        files (list): A list of all image files in the directory.
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
            content[last_subfolder].append(parts[-1])
    return content


def plot(directory, content):
    """
    Plot pie and bar charts for the class distribution.

    Parameters:
        directory (str): The directory name.
        content (dict): A dictionary with the last-level
            subfolder as keys and the number of files as values.
    Returns: None
    Raises: None
    """

    def plot_pie(directory, labels, values):
        """
        Plot a pie chart for the class distribution.

        Parameters:
            directory (str): The directory name.
            labels (list): A list of the last-level subfolders.
            values (list): A list of the number of files.
        Returns: None
        Raises: None
        """
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%',
                startangle=140, colors=colors)
        plt.title(f'{directory} class distribution', fontsize=16)
        plt.axis('equal')
        plt.savefig(os.path.join(RESULTS_DIRECTORY, PIE_CHART_FILENAME))
        plt.close()
        print(f"Distribution.py: Pie chart saved at "
              f"{RESULTS_RELATIVE_PATH}/{PIE_CHART_FILENAME}")

    def plot_bar(directory, labels, values):
        """
        Plot a bar chart for the class distribution.

        Parameters:
            directory (str): The directory name.
            labels (list): A list of the last-level subfolders.
            values (list): A list of the number of files.
        Returns: None
        Raises: None
        """
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=colors)
        plt.xlabel('Folders', fontsize=14)
        plt.ylabel('Number of files', fontsize=14)
        plt.title(f'{directory} class distribution', fontsize=16)
        plt.xticks(rotation=45, fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIRECTORY, BAR_CHART_FILENAME))
        plt.close()
        print(f"Distribution.py: Bar chart saved at "
              f"{RESULTS_RELATIVE_PATH}/{BAR_CHART_FILENAME}")

    labels = list(content.keys())
    values = [len(files) for files in content.values()]
    colors = plt.cm.Paired(range(len(labels)))

    os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
    plot_pie(directory, labels, values)
    plot_bar(directory, labels, values)


def main(directory):
    """
    Main function to extract and analyze the dataset from images
    and generate charts.

    Parameters:
        directory (str): The directory path.
    Returns: None
    Raises: None
    """
    files = fetch_files(directory)
    grouped_files = group_files(directory, files)
    plot(directory.split('/')[-1], grouped_files)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            prog="Distribution",
            description="Extract and analyze a dataset from \
                images and generate charts",
        )
        parser.add_argument("images_directory", type=str,
                            help="Path to the images directory")
        args = parser.parse_args()
        main(args.images_directory)

    except Exception as e:
        print(f"Distribution.py: error: {e}")
