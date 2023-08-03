# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/23 12:27
@Auth ： YY
@File ：SingleImagePixelEditingTool.py
@IDE ：PyCharm
@state:
@Function：
"""
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.uic import loadUi


class SingleImagePixelEditingTool(QWidget):
    # finishClick = pyqtSignal(str)

    def __init__(self, parent=None, ):
        super(SingleImagePixelEditingTool, self).__init__(parent)
        loadUi('GUI/SingleImagePixelEditingTool.ui', self)
