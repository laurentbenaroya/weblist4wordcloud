import os
import sys


def is_small_to_medium_text_file(filename, max_size=10 * 1024 * 1024):
    """
    Checks if a file is a small to medium-sized text file.

    Args:
        filename (str): Path to the file.
        max_size (int, optional): Maximum file size to consider as a text file. Defaults to 10 * 1024 * 1024 (10 MB).

    Returns:
        bool: True if the file is a text file and its size is within the given range, False otherwise.
    """

    # Check file size
    if os.path.getsize(filename) > max_size:
        return False

    # Check file content
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False

    return True


if __name__ == '__main__':
    # Example usage
    if len(sys.argv)< 2:
        sys.exit('Usage : python test_text_file.py xxx.txt')
    filename = sys.argv[1]
    if is_small_to_medium_text_file(filename):
        print(f'{filename} is a small to medium-sized text file')
    else:
        print(f'{filename} is not a small to medium-sized text file')
