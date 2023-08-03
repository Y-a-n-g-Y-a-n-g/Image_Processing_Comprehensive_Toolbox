# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/25 20:08
@Auth ： YY
@File ：ItemWidgets.py
@IDE ：PyCharm
@state:
@Function：存放各种ItemWidget类
"""
import os
import re

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QListWidget, QWidget, QHBoxLayout, \
    QPushButton, QMessageBox

from components.ImageProcessAndProcessRules import ImageProcessAndProcessRules


class PicturelistLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PicturelistLabel, self).__init__(parent)
        self.imagepath = ""

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.clicked.emit(self.imagepath)


class SeclectedDirItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, text, item, *args, **kwargs):
        super(SeclectedDirItemWidget, self).__init__(*args, **kwargs)
        self._item = item  # 保留list item的对象引用
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        labeltxt = QLabel(text, self)
        layout.addWidget(labeltxt)
        button = QPushButton('load images', self, clicked=self.loadimages)
        button.setMaximumSize(100, 20)
        layout.addWidget(button)

    def loadimages(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        return QSize(180, 20)


class PictureListWidget(QListWidget):
    finishClick = pyqtSignal(str)

    def __init__(self, dipath, mainwindow):
        super(PictureListWidget, self).__init__()
        self.setStyleSheet("background-color: rgb(50, 50, 50);")
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # item的间隔
        self.setSpacing(5)
        # 第一张图片的索引
        self.firstpicturenum = 0
        self.mainwindow = mainwindow

        self.dipath = dipath

    def ShowOnePicture(self, size, cname, path, dipath):
        self.path = path
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)  # 把颜色放进自定义的data里面
        item.setSizeHint(size)
        label = PicturelistLabel(self)  # 自定义控件
        label.imagepath = dipath + '/' + path
        label.clicked.connect(lambda: self.singlepicture(label))
        label.setMargin(2)
        label.resize(size)
        try:
            img = cv2.imread(dipath + '/' + path, cv2.IMREAD_UNCHANGED)
            shape = img.shape
            pictruetxt = []
            if self.mainwindow.checkBox_2.isChecked():
                pictruetxt.append(path)
            if self.mainwindow.checkBox.isChecked():
                dipath = dipath.replace('\\', '/')
                pictruetxt.append(re.split('/', dipath)[-1])
            if self.mainwindow.checkBox_3.isChecked():
                pictruetxt.append(f"{shape[1]}x{shape[0]}")
            img = cv2.resize(img, (250, 250), interpolation=cv2.INTER_CUBIC)
            for idx, txt in enumerate(pictruetxt):
                img = cv2.putText(img, txt, (5, 20 + idx * 20), 5, 1, (0, 255, 0), 1)
        except:
            img = cv2.imread("assets/ImageLoadError.png", cv2.IMREAD_UNCHANGED)
            img = cv2.resize(img, (330, 330), interpolation=cv2.INTER_CUBIC)
            img = cv2.putText(img, path, (5, 20), 5, 1, (0, 255, 0), 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (190, 190), interpolation=cv2.INTER_CUBIC)
        img_dis = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3,
                         QImage.Format_RGB888)
        img_dis = QPixmap(img_dis).scaled(img.shape[1], img.shape[0])
        label.setPixmap(img_dis)

        self.setItemWidget(item, label)

    def singlepicture(self, label):
        self.ImageProcessAndProcessRules = ImageProcessAndProcessRules(label.imagepath)
        self.ImageProcessAndProcessRules.finishClick.connect(self.update_rule)
        self.ImageProcessAndProcessRules.show()

    def initItems(self, dipath):
        size = QSize(190, 190)
        self.dipath = dipath
        self.clear()
        self.dirlist = os.listdir(self.dipath)
        self.endpictruenum = self.firstpicturenum + self.mainwindow.numpictureperpage[
            self.mainwindow.comboBox.currentIndex()] if self.mainwindow.numpictureperpage[
                                                            self.mainwindow.comboBox.currentIndex()] < len(
            self.dirlist) else len(self.dirlist)
        for i in range(self.firstpicturenum, self.endpictruenum):
            self.ShowOnePicture(size, self.dipath, self.dirlist[i], dipath)
        self.mainwindow.label_displaynum.setText(
            f"({self.firstpicturenum}~{self.firstpicturenum + self.mainwindow.numpictureperpage[self.mainwindow.comboBox.currentIndex()]})/{len(self.dirlist)}")


    def update_rule(self):
        self.finishClick.emit("")
