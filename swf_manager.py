#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os import listdir, rename
from shutil import *
from datetime import *
import time
from threading import *

Symbol_For_Path = "\ "

now_time = datetime.now()
cur_year = now_time.year
cur_month = now_time.month
cur_day = now_time.day
cur_hour = now_time.hour
cur_minute = now_time.minute
cur_seconds = now_time.second


class SecondThread(Thread):
    def __init__(self, name):
        Thread.__init__(self, name=name)
        self.times = 0

    def run(self):

        db_1 = open(r"Paths.txt", "r")
        db_1_readlines = db_1.readlines()
        dwn_path = db_1_readlines[0]
        Downloaded_SWF_Path = dwn_path[0:-1]
        ori_path = db_1_readlines[1]
        Original_SWF_Path = ori_path[0:-1]
        bck_path = db_1_readlines[2]
        Backup_Path = bck_path[0:-1]
        db_1.close()

        while self.times == 0:
            try:
                Files_Search = listdir(Downloaded_SWF_Path)
                Filter = list(filter(lambda x: x.endswith('.bmp'), Files_Search))
                Get_File_Name = Filter[0]
                Files_Search_2 = listdir(Original_SWF_Path)
                Filter_2 = list(filter(lambda x: x.endswith(Get_File_Name), Files_Search_2))
                rename(Original_SWF_Path +
                       str(Symbol_For_Path[0]) +
                       str(Get_File_Name),
                       "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}".format(Backup_Path,
                                                                               str(Symbol_For_Path[0]),
                                                                               str(Get_File_Name.replace(".bmp",
                                                                                                         "")),
                                                                               str("-"), str(cur_year),
                                                                               str("-"), str(cur_month),
                                                                               str("-"), str(cur_day),
                                                                               str("-"), str(cur_hour),
                                                                               str("-"), str(cur_minute),
                                                                               str(".bmp")))
                Go_To_Original = move("{0}{1}{2}".format(Downloaded_SWF_Path,
                                                         str(Symbol_For_Path[0]),
                                                         str(Get_File_Name)),
                                      Original_SWF_Path)
            except BaseException as e:
                print(e)
                time.sleep(5)

    def stop(self):
        self.times = 1

    def start_again(self):
        self.times = 0


ht = SecondThread('SecondThread')


class Button(QPushButton):

    def __init__(self, title, parent):

        super().__init__(title, parent)

        self.a = 0
        self.b = 0

    def hide_self(self):

        self.a = 1

        if self.a == 1:
            self.hide()
            pass

    def show_self(self):

        self.a = 0

        if self.a == 0:
            self.show()
            pass

    def disabled(self):

        self.b = 1

        if self.b == 1:
            self.setDisabled(True)
            pass

    def enabled(self):

        self.b = 0

        if self.b == 0:
            self.setDisabled(False)
            pass


class SWF_Copy_Manager(QMainWindow):
    def __init__(self):
        super().__init__()

        ##Задаем объекты размещаемые в нашем окне
        self.tray_icon = QSystemTrayIcon(self)
        self.le = QLineEdit(self)
        self.le2 = QLineEdit(self)
        self.le3 = QLineEdit(self)
        self.initUI()

    def initUI(self):

        ##Работа с файлами
        db_1 = open(r"Paths.txt", "r")
        db_1_readlines = db_1.readlines()
        dwn_path = db_1_readlines[0]
        Downloaded_SWF_Path = dwn_path[0:-1]
        ori_path = db_1_readlines[1]
        Original_SWF_Path = ori_path[0:-1]
        bck_path = db_1_readlines[2]
        Backup_Path = bck_path[0:-1]
        db_1.close()

        ##Задаем дефолтные значения для полей ввода текста
        self.le.move(150, 20)
        self.le.setText(str(Downloaded_SWF_Path))

        self.le2.move(150, 60)
        self.le2.setText(str(Original_SWF_Path))

        self.le3.move(150, 100)
        self.le3.setText(str(Backup_Path))

        ##Задаем параметры окна
        self.setStyleSheet("background-color:#FAF0E6;")
        self.statusBar().showMessage('Ready for fight')
        self.setFixedSize(600, 250)
        self.setWindowTitle('SWF Copy & Backup Manager')
        self.setWindowIcon(QIcon('75.png'))
        self.center()

        ##Заводим кнопки с действиями
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        quit_action = QAction("Exit", self)
        ##start_script = QAction("Start Script", self)
        ##pause_script = QAction("Start Script", self)
        ##stop_script = QAction("Stop Script", self)
        ##Создаем менюшку
        tray_menu = QMenu()
        ##tray_menu.addAction(start_script)
        ##tray_menu.addAction(pause_script)
        ##tray_menu.addAction(stop_script)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        ##Добавляем в трей менюшку и меняем иконку
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setIcon(QIcon('75.png'))

        ##Задаем шрифт тултипов и задаем тултипы под поля ввода
        QToolTip.setFont(QFont("SansSerif", 10))
        self.le.setToolTip('Folder with downloads *.swf files')
        self.le2.setToolTip('Folder with Original *.swf files')
        self.le3.setToolTip('Folder with backups *.swf files')

        ##Создаем кнопочки
        dw_btn = QPushButton(self)
        or_btn = QPushButton('Original Folder', self)
        bck_btn = QPushButton('Backup Folder', self)
        ps_btn = Button('Start', self)
        lch_btn = Button('Start', self)
        stp_btn = Button('Stop', self)
        hd_btn = Button('Hide', self)

        ##Присваиваем кнопочкам действия и другие атрибуты
        dw_btn.setToolTip("Set folder with downloads *.swf files")
        dw_btn.move(5, 10)
        dw_btn.setStyleSheet("background-color:#FAF0E6;")
        dw_btn.setFixedSize(38, 38)
        dw_btn.setIcon(QIcon('folder_blue_favorites.png'))
        dw_btn.setIconSize(QSize(38, 38))
        dw_btn.clicked.connect(self.showDialog)

        or_btn.setToolTip("Set folder with Original *.swf files")
        or_btn.move(20, 60)
        or_btn.clicked.connect(self.showDialog2)

        bck_btn.setToolTip("Set folder with backups *.swf files")
        bck_btn.move(20, 100)
        bck_btn.clicked.connect(self.showDialog3)

        ps_btn.hide()
        ps_btn.setDisabled(True)
        ps_btn.move(20, 180)
        ps_btn.clicked.connect(ht.start_again)
        ps_btn.clicked.connect(stp_btn.enabled)
        ps_btn.clicked.connect(ps_btn.disabled)

        lch_btn.setToolTip("This button will start script to work")
        lch_btn.move(20, 180)
        lch_btn.clicked.connect(ht.start)
        lch_btn.clicked.connect(lch_btn.hide_self)
        lch_btn.clicked.connect(ps_btn.show_self)
        lch_btn.clicked.connect(stp_btn.enabled)

        stp_btn.setToolTip('This button will stop script to work')
        stp_btn.move(150, 180)
        stp_btn.setDisabled(True)
        stp_btn.clicked.connect(ht.stop)
        stp_btn.clicked.connect(ps_btn.enabled)
        stp_btn.clicked.connect(stp_btn.disabled)

        hd_btn.setToolTip("This button hides app")
        hd_btn.move(20, 150)
        hd_btn.clicked.connect(self.hide_self)
        hd_btn.clicked.connect(self.tray_icon_hide_show)

        ##Задаем экшен для кнопок в трей менюшке
        show_action.triggered.connect(self.show)
        show_action.triggered.connect(self.tray_icon_hide_show)

        hide_action.triggered.connect(self.hide)

        quit_action.triggered.connect(qApp.quit)

    def showDialog(self):
        self.statusBar().showMessage('Input path')
        text, ok = QInputDialog.getText(self, "Set path",
                                        "Enter path for Download folder:")
        if ok:
            self.statusBar().showMessage('Path changed')
            self.le.setText(str(text))

            db_1 = open(r"Paths.txt", "r")
            db_1_readlines = db_1.readlines()
            db_1.close()

            db_1_readlines[0] = str(text) + "\n"

            db_1 = open(r"Paths.txt", "w")
            db_1.writelines(db_1_readlines)
            db_1.close()

    def showDialog2(self):
        self.statusBar().showMessage('Input path')
        text, ok = QInputDialog.getText(self, "Set path",
                                        "Enter path for Download folder:")
        if ok:
            self.statusBar().showMessage('Path changed')
            self.le2.setText(str(text))

            db_1 = open(r"Paths.txt", "r")
            db_1_readlines = db_1.readlines()
            db_1.close()

            db_1_readlines[1] = str(text) + "\n"

            db_1 = open(r"Paths.txt", "w")
            db_1.writelines(db_1_readlines)
            db_1.close()

    def showDialog3(self):
        self.statusBar().showMessage('Input path')
        text, ok = QInputDialog.getText(self, "Set path",
                                        "Enter path for Download folder:")
        if ok:
            self.statusBar().showMessage('Path changed')
            self.le3.setText(str(text))

            db_1 = open(r"Paths.txt", "r")
            db_1_readlines = db_1.readlines()
            db_1.close()

            db_1_readlines[2] = str(text) + "\n"

            db_1 = open(r"Paths.txt", "w")
            db_1.writelines(db_1_readlines)
            db_1.close()

    def closeEvent(self, event):

        reply = QMessageBox.question(self,
                                     'Exit',
                                     "Do you really want to leave?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            ht.stop()
            event.accept()
        else:
            event.ignore()

    def tray_icon_hide_show(self):
            if self.isHidden():
                self.tray_icon.show()
            else:
                self.tray_icon.hide()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.hide()
                return

    def hide_self(self):
        self.hide()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SWF_Copy_Manager()
    ex.show()
    sys.exit(app.exec_())
