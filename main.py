import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi

from components import Global_Var_Func
from components.Global_Var_Func import Rotate, MirrorH, MirrorV, Scaling, imgBrightness
from components.ItemWidgets import *
from components.SelectDirectoryDialog import SelectDirectoryDialog

Global_Var_Func._init()
Global_Var_Func.set_value('Rule', {})
current_directory = os.getcwd()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('GUI/GUI.ui', self)
        # 菜单栏控件连接函数
        self.actionOpen_Directory.triggered.connect(self.act_loadfiles)
        self.actionOpen_File.triggered.connect(self.act_loadfile)
        self.actionReplace_the_original_file_and_save_it.triggered.connect(
            self.act_Replace_the_original_file_and_save_it)
        self.actionSave_as_according_to_the_original_file_path_structure.triggered.connect(
            self.act_Save_as_according_to_the_original_file_path_structure)
        # 按钮信号连接到响应函数
        self.btn_lastpage.clicked.connect(self.lastpage)
        self.btn_nextpage.clicked.connect(self.nextpage)
        self.btn_reloadimg.clicked.connect(self.f_btn_reloadimg)
        self.btn_updaterule.clicked.connect(self.update_rule)
        self.btn_batchprocess.clicked.connect(self.batchprocessimgs)
        # 初始化图片列表控件
        self.PictureListWidget = PictureListWidget('', self)
        self.PictureListWidget.finishClick.connect(self.update_rule)
        self.verticalLayout.addWidget(self.PictureListWidget)
        # 一些参数储存
        self.paths = []
        self.comboBox.addItems(["100 per page", "500 per page", "1000 per page", "1500 per page", "3000 per page"])
        self.numpictureperpage = [100, 500, 1000, 1500, 3000]

    def act_loadfile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Please select the image to be processed', current_directory,
                                               'Image files (*.jpg;*.BMP;*.JPEG;*.PNG;*.PPM;*.XBM;*.XPM;)')
        if fname:
            self.ImageProcessAndProcessRules = ImageProcessAndProcessRules(fname)
            self.ImageProcessAndProcessRules.finishClick.connect(self.update_rule)
            self.ImageProcessAndProcessRules.show()

    def act_loadfiles(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Please select a folder path", current_directory)
        if directory:
            self.paths = []
            for dirpath, dirnames, filenames in os.walk(directory):
                self.paths.append(dirpath)
            self.SelectDirectoryDialog = SelectDirectoryDialog(paths=self.paths)
            self.SelectDirectoryDialog.setModal(True)
            self.SelectDirectoryDialog.show()
            self.SelectDirectoryDialog.mySignal.connect(self.hanleselect_directory)

    def hanleselect_directory(self, msg):
        for idx, flag in enumerate(msg):
            if flag == True:
                item = QListWidgetItem(self.SelectedDirlistWidget)
                item.setToolTip(self.paths[idx])
                item.imagesdirpath = self.paths[idx]
                widget = SeclectedDirItemWidget(self.paths[idx], item, self.SelectedDirlistWidget)
                widget.itemDeleted.connect(self.loadimage)
                self.SelectedDirlistWidget.setItemWidget(item, widget)

    def loadimage(self, item):
        self.PictureListWidget.firstpicturenum = 0
        self.PictureListWidget.initItems(item.imagesdirpath)

    def f_btn_reloadimg(self):
        self.PictureListWidget.initItems(self.PictureListWidget.dipath)
        # self.PictureListWidget.initItems()

    def act_Replace_the_original_file_and_save_it(self):
        pass

    def act_Save_as_according_to_the_original_file_path_structure(self):
        pass

    def update_rule(self):
        self.rules = Global_Var_Func.get_value('Rule')
        self.comboBox_Rules.addItems(self.rules.keys())
        print("Rule updated")

    def lastpage(self):
        self.PictureListWidget.firstpicturenum = self.PictureListWidget.firstpicturenum - w.numpictureperpage[
            w.comboBox.currentIndex()]
        self.PictureListWidget.firstpicturenum = 0 if self.PictureListWidget.firstpicturenum < 0 else self.PictureListWidget.firstpicturenum
        self.PictureListWidget.initItems(self.PictureListWidget.dipath)

    def nextpage(self):
        if self.PictureListWidget.endpictruenum == len(self.PictureListWidget.dirlist):
            QMessageBox.critical(self, "ERROR", "No more pictures!")
        else:
            self.PictureListWidget.firstpicturenum = self.PictureListWidget.firstpicturenum + w.numpictureperpage[
                w.comboBox.currentIndex()]
            self.PictureListWidget.initItems(self.PictureListWidget.dipath)

    def batchprocessimgs(self):
        Dirname = QFileDialog.getExistingDirectory(None, "Select a folder to save the processed files", os.getcwd())
        picturepath = self.PictureListWidget.dipath
        Rules = self.rules[self.comboBox_Rules.currentText()]
        # print(Dirname,picturepath,Rules)
        if Dirname != '':
            successnum = 0
            failnames = []
            Brightnessfails = []
            for failename in os.listdir(picturepath):
                try:
                    img = cv2.imread(picturepath + '/' + failename, cv2.IMREAD_UNCHANGED)
                    for rule in Rules:
                        ruletype, rulevalue = re.split(":", Rules[rule])
                        # print(ruletype,rulevalue)
                        if ruletype == "Rotate":
                            img = Rotate(img, int(rulevalue))
                        if ruletype == "Mirror" and rulevalue == "H":
                            img = MirrorH(img)
                        if ruletype == "Mirror" and rulevalue == "V":
                            img = MirrorV(img)
                        if ruletype == "Scaling":
                            img = Scaling(img, int(rulevalue.replace("%", "")))
                        if ruletype == "BrightAdjust":
                            try:
                                img = imgBrightness(img, int(rulevalue.replace("%", "")) / 100, 3)
                            except:
                                Brightnessfails.append(failename)

                    cv2.imwrite(Dirname + '/' + failename, img)
                    successnum = successnum + 1
                except:
                    failnames.append(failename)

        QMessageBox.information(self, "Finish",
                                f"Process {len(os.listdir(picturepath))} files, {successnum} files successfully",
                                QMessageBox.Ok)
        print(failnames)
        print(Brightnessfails)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
