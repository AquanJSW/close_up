"""Filtering close-up images w.r.t. msl-mastcam"""

import os
import shutil
from tqdm import tqdm as tqdm
from cahv import main as cahv
from angle import main as angle
from mypylib.myfunc import file_counter

LBL_DIR = 'D:\\Datasets\\labels\\'
LBL_SUFFIX = '_XXXX.LBL'
IMG_DIR = 'D:\\Datasets\\0\\'
THRESHOLD = (30, 40, 50, 60, 65, 70, 75, 80, 85)


def judge(img_name):
    """Image's label file existence judgement. Also calculate degree(C)

    :return: `[True, degree]` if label file exist, otherwise `[False, None]`
    """

    lbl_name = img_name.split('_')[0] + LBL_SUFFIX
    lbl_path = LBL_DIR + lbl_name

    if os.path.exists(lbl_path):
        model = cahv(lbl_path)

        if not model:
            return[False, None]

        degree = angle(coordinate=model['A'], axis=2, module=True)

        if not degree:
            print("something wrong with image `%s`" % img_name)
            return [False, None]

        return [True, degree]
    else:
        return [False, None]


def mkdir():
    """Make sub-directories w.r.t. `THRESHOLD`"""

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
    return subdirs


def classify(path, degree, subdirs):
    """Classify image to corresponding sub-directory according to its degree"""

    for idx in range(len(THRESHOLD)):
        if degree < THRESHOLD[idx]:
            shutil.move(path, subdirs[idx])
            break
        else:
            continue


def main():
    subdirs = mkdir()
    pbar = tqdm(total=file_counter(IMG_DIR))

    with os.scandir(IMG_DIR) as entries:
        for entry in entries:
            pbar.update()
            judgement = judge(entry.name)

            if judgement[0]:
                classify(path=entry.path, degree=judgement[1], subdirs=subdirs)


if __name__ == "__main__":
    main()
