# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/19 13:33
@Auth ： YY
@File ：ImageProcessAndProcessRules.py
@IDE ：PyCharm
@State: Finish
@Function：用于处理单张图片或生成批量处理图片的规则
"""

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QLabel, QListWidgetItem, QWidget, QHBoxLayout, QLineEdit, QPushButton, \
    QFileDialog, QInputDialog, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from pyqt5_plugins.examplebuttonplugin import QtGui

import components.Global_Var_Func as Global_Var_Func
from components.SingleImagePixelEditingTool import SingleImagePixelEditingTool


class ItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, text, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self._item = item  # 保留list item的对象引用
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        labeltxt = QLineEdit(text, self)
        labeltxt.resize(160, 20)
        layout.addWidget(labeltxt)
        button = QPushButton('x', self, clicked=self.doDeleteItem)
        button.setMaximumSize(20, 20)
        layout.addWidget(button)

    def doDeleteItem(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        # 决定item的高度
        return QSize(180, 20)


class ImageProcessAndProcessRules(QMainWindow):
    finishClick = pyqtSignal(str)

    def __init__(self, imagepath, parent=None, ):
        super(ImageProcessAndProcessRules, self).__init__(parent)
        loadUi('GUI/ImageProcessAndProcessRules.ui', self)
        # 保存处理步骤
        self.stepnum = 0
        # 保存处理历史照片
        self.stephistory = {}
        self.historyimage = []
        self.historyimagewithlable = []
        # 读取图片
        self.img = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)
        # 显示图片
        self.showpictrue(self.img)
        img = self.img.copy()
        img = cv2.putText(img, "Raw", (10, 80), 5, 5, (0, 255, 0), 3)
        self.historyimage.append(self.img)
        self.historyimagewithlable.append(img)
        self.makeItem(QSize(100, 100), img)
        self.historyprocessstep.setStyleSheet("background-color: rgb(100, 100, 100);")
        # 设置从左到右、自动换行、依次排列
        self.historyprocessstep.setFlow(self.historyprocessstep.LeftToRight)
        self.historyprocessstep.setWrapping(True)
        self.historyprocessstep.setResizeMode(self.historyprocessstep.Adjust)
        # item的间隔
        self.historyprocessstep.setSpacing(3)
        # 连接信号与槽
        self.pushButton.clicked.connect(lambda: self.btn_Rotate(90))
        self.pushButton_2.clicked.connect(lambda: self.btn_Rotate(180))
        self.pushButton_3.clicked.connect(lambda: self.btn_Rotate(270))
        self.pushButton_4.clicked.connect(self.btn_MirrorH)
        self.pushButton_5.clicked.connect(self.btn_MirrorV)
        self.pushButton_7.clicked.connect(lambda: self.btn_Scaling(85))
        self.pushButton_8.clicked.connect(lambda: self.btn_Scaling(70))
        self.pushButton_9.clicked.connect(lambda: self.btn_Scaling(55))
        self.pushButton_10.clicked.connect(lambda: self.btn_Scaling(40))
        self.pushButton_11.clicked.connect(lambda: self.btn_Scaling(115))
        self.pushButton_12.clicked.connect(lambda: self.btn_Scaling(130))
        self.pushButton_13.clicked.connect(lambda: self.btn_Scaling(145))
        self.pushButton_14.clicked.connect(lambda: self.btn_BrightAdjustment(110))
        self.pushButton_15.clicked.connect(lambda: self.btn_BrightAdjustment(120))
        self.pushButton_16.clicked.connect(lambda: self.btn_BrightAdjustment(130))
        self.pushButton_17.clicked.connect(lambda: self.btn_BrightAdjustment(140))
        self.pushButton_18.clicked.connect(lambda: self.btn_BrightAdjustment(150))
        self.pushButton_19.clicked.connect(lambda: self.btn_BrightAdjustment(90))
        self.pushButton_20.clicked.connect(lambda: self.btn_BrightAdjustment(80))
        self.pushButton_21.clicked.connect(lambda: self.btn_BrightAdjustment(70))
        self.pushButton_22.clicked.connect(lambda: self.btn_BrightAdjustment(60))
        self.pushButton_23.clicked.connect(lambda: self.btn_BrightAdjustment(50))
        self.pushButton_27.clicked.connect(self.saveimage)
        self.pushButton_28.clicked.connect(self.saverule)
        self.pushButton_29.clicked.connect(self.finishedit)
        self.btn_pixelmodify.clicked.connect(self.f_btn_pixelmodify)

    def f_btn_pixelmodify(self):
        self.SingleImagePixelEditingTool = SingleImagePixelEditingTool()
        self.SingleImagePixelEditingTool.pixeltableWidget.setColumnCount(self.img.shape[1])  # 设置列数
        self.SingleImagePixelEditingTool.pixeltableWidget.setRowCount(self.img.shape[0])  # 设置行数
        self.SingleImagePixelEditingTool.pixeltableWidget.horizontalHeader().setDefaultSectionSize(2)
        self.SingleImagePixelEditingTool.pixeltableWidget.verticalHeader().setDefaultSectionSize(2)
        self.SingleImagePixelEditingTool.pixeltableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.SingleImagePixelEditingTool.pixeltableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        hight = self.img.shape[0]
        width = self.img.shape[1]
        channels = self.img.shape[2]
        for row in range(hight):  # 循环改变每个像素点的RGB值
            for col in range(width):
                pv = self.img[row, col]
                # print(pv)
                self.SingleImagePixelEditingTool.pixeltableWidget.setItem(row, col, QTableWidgetItem())
                self.SingleImagePixelEditingTool.pixeltableWidget.item(row, col).setBackground(
                    QtGui.QBrush(QtGui.QColor(pv[2], pv[1], pv[0])))
        self.SingleImagePixelEditingTool.show()

    def makeItem(self, size, pic):
        item = QListWidgetItem(self.historyprocessstep)
        item.setData(Qt.UserRole + 1, pic)  # 把颜色放进自定义的data里面
        item.setSizeHint(size)
        label = QLabel(self.historyprocessstep)  # 自定义控件
        label.setMargin(2)  # 往内缩进2
        label.resize(size)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        pic = cv2.resize(pic, (96, 96), interpolation=cv2.INTER_CUBIC)
        img_dis = QImage(pic, pic.shape[1], pic.shape[0], pic.shape[1] * 3,
                         QImage.Format_RGB888)
        img_dis = QPixmap(img_dis).scaled(pic.shape[1], pic.shape[0])
        label.setPixmap(img_dis)
        self.historyprocessstep.setItemWidget(item, label)

    def AddHistoryImageItem(self):
        self.historyprocessstep.clear()
        size = QSize(100, 100)
        for pic in self.historyimagewithlable:
            self.makeItem(size, pic)

    def backupprocessimage(self, operation):
        self.stepnum = 1 + self.stepnum
        self.stephistory[f"Step:{self.stepnum}"] = operation
        item = QListWidgetItem(self.setphistoryList)
        widget = ItemWidget('Step:{} {}'.format(self.stepnum, operation), item, self.setphistoryList)
        # 绑定删除信号
        widget.itemDeleted.connect(self.doDeleteItem)
        self.setphistoryList.setItemWidget(item, widget)
        img = self.img.copy()
        img = cv2.resize(img, (96, 96), interpolation=cv2.INTER_CUBIC)
        img = cv2.putText(img, f"Step{self.stepnum}", (10, 20), 5, 1, (0, 255, 0), 1)
        self.historyimagewithlable.append(img)
        self.historyimage.append(self.img)
        self.AddHistoryImageItem()

    def doDeleteItem(self, widget):
        # 根据item得到它对应的行数
        row = self.setphistoryList.indexFromItem(widget).row()
        # 删除item
        item = self.setphistoryList.takeItem(row)
        item2 = self.historyprocessstep.takeItem(row + 1)
        # 删除widget
        self.setphistoryList.removeItemWidget(item)
        self.historyprocessstep.removeItemWidget(item2)
        self.historyimage.pop(row + 1)
        self.historyimagewithlable.pop(row + 1)
        self.showpictrue(self.historyimage[-1])
        self.img = self.historyimage[-1]
        del self.stephistory[f"Step:{row + 1}"]
        del item, item2

    def showpictrue(self, img):
        self.rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_dis = QImage(self.rgb_img, self.rgb_img.shape[1], self.rgb_img.shape[0], self.rgb_img.shape[1] * 3,
                         QImage.Format_RGB888)
        img_dis = QPixmap(img_dis).scaled(self.rgb_img.shape[1], self.rgb_img.shape[0])
        self.picture.setPixmap(img_dis)

    def btn_Rotate(self, param):
        self.img = np.rot90(self.img, -param / 90)
        self.showpictrue(self.img)
        self.backupprocessimage(f'Rotate:{param}')

    def btn_MirrorV(self):
        self.img = cv2.flip(self.img, 1)
        self.showpictrue(self.img)
        self.backupprocessimage(f'Mirror:V')

    def btn_MirrorH(self):
        self.img = cv2.flip(self.img, 0)
        self.showpictrue(self.img)
        self.backupprocessimage(f'Mirror:H')

    def btn_Scaling(self, param):
        self.img = cv2.resize(self.img, (0, 0), fx=param / 100.0, fy=param / 100.0, interpolation=cv2.INTER_CUBIC)
        self.showpictrue(self.img)
        self.backupprocessimage(f'Scaling:{param}%')

    def btn_BrightAdjustment(self, param):
        self.img = Global_Var_Func.imgBrightness(self.img, param / 100, 3)
        self.showpictrue(self.img)
        self.backupprocessimage(f'BrightAdjust:{param}%')

    def saverule(self):
        text, okPressed = QInputDialog.getText(self, "Enter the rule code", "Please enter English letters or numbers:",
                                               QLineEdit.Normal, "Rule1")
        if okPressed and text != '':
            item = QListWidgetItem(self.listWidget)
            widget = ItemWidget(text, item, self.listWidget)
            # 绑定删除信号
            widget.itemDeleted.connect(self.doDeleteItem)
            self.listWidget.setItemWidget(item, widget)
            rules=Global_Var_Func.get_value('Rule')
            rules[text]=self.stephistory
            Global_Var_Func.set_value('Rule', rules)
            # print(Global_Var_Func.get_value('Rule'))

    def saveimage(self):
        fname, ftype = QFileDialog.getSaveFileName(self, 'save file', './', "image type (*.jpg)")
        if fname != '':
            cv2.imwrite(fname, self.img)

    def finishedit(self):
        self.finishClick.emit("")
        self.close()
