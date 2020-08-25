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
THRESHOLD = 70
OUT_DIR = IMG_DIR + "%s" % THRESHOLD + '\\'


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

        if degree < THRESHOLD:
            return [True, degree]
        else:
            return [False, ]

    else:
        return [False, ]


def main():
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    pbar = tqdm(total=file_counter())

    with os.scandir(IMG_DIR) as entries:
        for entry in entries:
            pbar.update()
            judgement = judge(entry.name)
            if judgement[0]:
                shutil.move(entry.path, OUT_DIR)


if __name__ == "__main__":
    main()
