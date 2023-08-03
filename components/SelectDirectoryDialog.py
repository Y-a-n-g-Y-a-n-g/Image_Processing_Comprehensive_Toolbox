# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/19 10:09
@Auth ： YY
@File ：SelectDirectoryDialog.py
@IDE ：PyCharm
@Function：用于获取选定主目录下需要进行文件处理的子目录
"""
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QCheckBox, QDialog, QMessageBox
from PyQt5.uic import loadUi


class SelectDirectoryDialog(QDialog):
    # 定义窗口选定子目录后发送给主窗口的信号
    mySignal = pyqtSignal(list)

    def __init__(self, paths, parent=None):
        super(SelectDirectoryDialog, self).__init__(parent)
        loadUi('GUI/SelectDirectoryDialog.ui', self)
        self.checkboxs = []
        self._model = QStandardItemModel(self)
        self.listView.setModel(self._model)
        self.setWindowTitle("Please select the file directory where you want to load the image.")
        self.buttonBox.accepted.connect(self.onAccepted)  # 选择完文件后的用户操作
        self.buttonBox.rejected.connect(self.onRejected)
        # 将传入的文件路径生成控件列表
        for i in paths:
            for dirpath, dirnames, filenames in os.walk(i):
                file_counts = len(filenames)
            item = QStandardItem()
            self._model.appendRow(item)  # 添加item
            index = self._model.indexFromItem(item)
            widget = QCheckBox(f'[{file_counts:>7d} files] ' + str(i))
            self.checkboxs.append(widget)
            widget.clicked.connect(lambda: self.onChecked(self.sender()))
            item.setSizeHint(widget.sizeHint())
            self.listView.setIndexWidget(index, widget)

    def onChecked(self, checkbox):
        if checkbox.isChecked():
            checkbox.setStyleSheet("background-color: rgb(170, 255, 127);")
        else:
            checkbox.setStyleSheet("")

    def onAccepted(self):
        # 检查每个控件的选定信息,生成列表传递给主窗口
        checkboxstatelist = []
        for checkbox in self.checkboxs:
            checkboxstatelist.append(checkbox.isChecked())
        self.mySignal.emit(checkboxstatelist)

    def onRejected(self):
        pass
