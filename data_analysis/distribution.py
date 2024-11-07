import os
import sys
import argparse
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils


RESULSTS_PATH = "images_analysis"
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
RESULTS_DIRECTORY = f"{CURRENT_WORKING_DIRECTORY}/../{RESULSTS_PATH}"
PIE_CHART_FILENAME = "pie_chart.png"
BAR_CHART_FILENAME = "bar_chart.png"


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
              f"{RESULSTS_PATH}/{PIE_CHART_FILENAME}")

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
              f"{RESULSTS_PATH}/{BAR_CHART_FILENAME}")

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
    utils.check_directory(directory)
    files = utils.fetch_files(directory)
    grouped_files = utils.group_files(directory, files)
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
