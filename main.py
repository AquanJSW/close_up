"""Filtering close-up images w.r.t. msl-mastcam"""

import os
import shutil
from tqdm import tqdm as tqdm
from cahv import main as cahv
from angle import main as angle
from mypylib import file_counter

LBL_DIR = 'D:\\Datasets\\labels\\'
LBL_SUFFIX = '_XXXX.LBL'
IMG_DIR = 'D:\\Datasets\\3\\'
THRESHOLD = (30, 40, 50, 60, 65, 70, 75, 80, 85)


def judge(img_name):
    """Image's label file existence judgement. Also calculate degree(C)

    :return: Position 0: `False` if label file not exist, `True` otherwise.
        Position 1: `None` if encountering some error during calculation, `degree` otherwise.
    """

    lbl_name = img_name.split('_')[0] + LBL_SUFFIX
    lbl_path = LBL_DIR + lbl_name

    if os.path.exists(lbl_path):
        model = cahv(lbl_path)

        if not model:
            return [True, None]

        degree = angle(coordinate=model['A'], axis=2, module=True)

        if not degree:
            print("something wrong with image `%s`" % img_name)
            return [True, None]

        return [True, degree]
    else:
        return [False, None]


def mkdir():
    """Make sub-directories w.r.t. `THRESHOLD`

    Additional two sub-directories are `without_label and `label_parsing_error`
    """

    subdirs = list()

    for idx in range(len(THRESHOLD)):
        if idx == 0:
            subdir_name = str(THRESHOLD[idx])

            if not os.path.exists(IMG_DIR + subdir_name):
                os.makedirs(IMG_DIR + subdir_name)

            subdirs.append(IMG_DIR + subdir_name)
        else:
            subdir_name = "%s-%s" % (str(THRESHOLD[idx-1]),
                                     str(THRESHOLD[idx]))

            if not os.path.exists(IMG_DIR + subdir_name):
                os.makedirs(IMG_DIR + subdir_name)

            subdirs.append(IMG_DIR + subdir_name)

    subdir_name = 'without_label'

    if not os.path.exists(IMG_DIR + subdir_name):
        os.makedirs(IMG_DIR + subdir_name)

    subdirs.append(IMG_DIR + subdir_name)

    subdir_name = 'label_parsing_error'

    if not os.path.exists(IMG_DIR + subdir_name):
        os.makedirs(IMG_DIR + subdir_name)

    subdirs.append(IMG_DIR + subdir_name)

    return subdirs


def classify(path, judgement, subdirs):
    """Classify image to corresponding sub-directory according to its degree"""

    existence, degree = judgement
    subdir_without_label, subdir_label_parsing_error = subdirs[-2:]

    if existence:
        if degree:
            for idx in range(len(THRESHOLD)):
                if degree < THRESHOLD[idx]:
                    shutil.move(path, subdirs[idx])
                    return None
        else:
            shutil.move(path, subdir_label_parsing_error)
            return None
    else:
        shutil.move(path, subdir_without_label)


def main():
    subdirs = mkdir()
    pbar = tqdm(total=file_counter(IMG_DIR))

    with os.scandir(IMG_DIR) as entries:
        for entry in entries:
            if entry.is_file():
                pbar.update()

                judgement = judge(entry.name)
                classify(path=entry.path, judgement=judgement, subdirs=subdirs)


if __name__ == "__main__":
    main()
