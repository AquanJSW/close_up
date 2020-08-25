"""Filtering close-up images w.r.t. mastcam"""

import os
import re
import shutil
from tqdm import tqdm as tqdm
from cahv import main as cahv
from angle import main as angle

LBL_DIR = 'D:\\Datasets\\labels\\'
LBL_SUFFIX = '_XXXX.LBL'
IMG_DIR = 'D:\\Datasets\\0\\'
THRESHOLD = (30, 40, 50, 60, 65, 70, 75, 80, 85)


def file_counter():
    count = 0
    with os.scandir(IMG_DIR) as entries:
        for entry in entries:
            if entry.is_file:
                count += 1
        return count


def judge(img_name):

    lbl_name = img_name.split('_')[0] + LBL_SUFFIX
    lbl_path = LBL_DIR + lbl_name

    if os.path.exists(lbl_path):

        model = cahv(lbl_path)
        if not model:
            return[False, ]

        degree = angle(coordinate=model['A'], axis=2, api=True)

        if not degree:
            print("something wrong with image `%s`" % img_name)
            return [False, ]
        return [True, degree]

    else:
        return [False, ]


def mkdir():
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
    for idx in range(len(THRESHOLD)):
        if degree < THRESHOLD[idx]:
            shutil.move(path, subdirs[idx])
            break
        else:
            continue


def main():
    subdirs = mkdir()
    pbar = tqdm(total=file_counter())

    with os.scandir(IMG_DIR) as entries:
        for entry in entries:
            pbar.update()
            judgement = judge(entry.name)
            if judgement[0]:
                classify(path=entry.path, degree=judgement[1], subdirs=subdirs)


if __name__ == "__main__":
    main()
