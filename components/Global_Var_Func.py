# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/20 17:14
@Auth ： YY
@File ：Global_Var_Func.py
@IDE ：PyCharm
@Function：用于在多文件中共享变量和函数
"""
import cv2
import numpy as np


def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    # 定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    # 获得一个全局变量，不存在则提示读取对应变量失败
    try:
        return _global_dict[key]
    except:
        print('读取' + key + '失败\r\n')


def imgBrightness(img1, c, b):
    rows, cols, channels = img1.shape
    blank = np.zeros([rows, cols, channels], img1.dtype)
    return cv2.addWeighted(img1, c, blank, 1 - c, b)


def Rotate(img, param):
    return np.rot90(img, -param / 90)


def MirrorV(img):
    return cv2.flip(img, 1)


def MirrorH(img):
    return cv2.flip(img, 0)


def Scaling(img, param):
    return cv2.resize(img, (0, 0), fx=param / 100.0, fy=param / 100.0, interpolation=cv2.INTER_CUBIC)
