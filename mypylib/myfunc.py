"""My Python functions"""

import os


def file_counter(dir):
    """File number counter
    
    :param dir: target directory
    :return: the number of files
    """
    count = 0
    with os.scandir(dir) as dir_entry:
        for entry in dir_entry:
            if entry.is_file:
                count += 1
    return count


def dir_counter(dir):
    """Directory number counter
    
    :param dir: target directory
    :return: the number of directories
    """
    count = 0
    with os.scandir(dir) as dir_entry:
        for entry in dir_entry:
            if entry.is_dir:
                count += 1
    return count
