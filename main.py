# This Python file uses the following encoding: utf-8
import sys
import os
from Database import Database
from Add_User import AddUser

from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QIcon
from functools import partial
from datetime import datetime


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('main.ui')
        self.ui.show()
        self.ui.setWindowIcon(QtGui.QIcon('assets/img/icon.png'))
        # self.ui.btn_light.setIcon(QIcon('assets/img/light_mode.png'))
        # self.ui.btn_del_all.setIcon(QIcon('assets/img/delete.png'))

        self.ui.btn_add.clicked.connect(self.addNewUser)
        self.users = self.readMessages()
        self.length = len(self.users)
        # self.ui.txt_message.installEventFilter(self)

    def readMessages(self):
        users = Database.select()
        print(users)
        for i, user in enumerate(users):
            label = QLabel()
            label.setText(user[1])
            self.ui.gl_users.addWidget(label, i, 1, alignment=Qt.Alignment())

            btn = QPushButton()
            btn.setText('×')
            btn.setStyleSheet('max-width: 18px; min-height: 18px; background-color: #F05454;'
                              ' color: white; border: 0px; border-radius: 5px;')

            self.ui.gl_users.addWidget(btn, i, 0, alignment=Qt.Alignment())
            btn.clicked.connect(partial(self.deleteMessage, user[0], btn, label))
        return users

    def addNewUser(self):
        print('in add new user-----------')
        AddUser.addNewUser()



    def deleteMessage(self, id, btn, label):
        response = Database.delete(id)
        if response:
            btn.hide()
            label.hide()
            self.msgBox("Your message deleted!")
        else:
            self.msgBox("Database error!")

    def deleteAllMessage(self):
        response = Database.deleteAll()
        if response:
            self.msgBox("all of messages deleted!")
            self.readMessages()

            for i in range(self.ui.gl_messages.count()):
                self.ui.gl_messages.itemAt(i).widget().hide()
        else:
            self.msgBox("Database error!")

    def changeTheme(self):
        if self.lightTheme:
            self.ui.setStyleSheet('background-color: #282846;')
            self.ui.btn_send.setStyleSheet(
                'background-color: #007580; color: #d8ebe4; border-radius: 3px; border: 0px;')
            self.ui.lbl_caption.setStyleSheet('background-color: #007580; color: #d8ebe4;')
            self.ui.lbl_header.setStyleSheet('background-color: #007580; border-radius: 5px; border: 0px;')
            self.ui.btn_del_all.setStyleSheet('background-color: #007580; border: 0px;')
            self.ui.btn_light.setStyleSheet('background-color: #007580; border: 0px;')

            for i in range(self.ui.gl_messages.count()):
                if type(self.ui.gl_messages.itemAt(i).widget()) == QLabel:
                    self.ui.gl_messages.itemAt(i).widget().setStyleSheet('color: #fff;')
        else:
            self.ui.setStyleSheet('background-color: #fad586;')
            self.ui.btn_send.setStyleSheet(
                'background-color: #184d47; color: #96bb7c; border-radius: 3px; border: 0px;')
            self.ui.lbl_caption.setStyleSheet('background-color: #184d47; color: #96bb7c;')
            self.ui.lbl_header.setStyleSheet('background-color: #184d47; border-radius: 5px; border: 0px;')
            self.ui.btn_del_all.setStyleSheet('background-color: #184d47; border: 0px;')
            self.ui.btn_light.setStyleSheet('background-color: #184d47; border: 0px;')

            for i in range(self.ui.gl_messages.count()):
                if type(self.ui.gl_messages.itemAt(i).widget()) == QLabel:
                    self.ui.gl_messages.itemAt(i).widget().setStyleSheet('color: #000;')

        self.lightTheme = not self.lightTheme

    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec())
