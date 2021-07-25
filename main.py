# This Python file uses the following encoding: utf-8
import sys
from Database import Database
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from functools import partial


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('main.ui')
        self.ui.show()
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

            btn = QPushButton()
            btn.setText('×')
            btn.setStyleSheet('max-width: 18px; min-height: 18px; background-color: #F05454;'
                              ' color: white; border: 0px; border-radius: 9px;')

            avatar = QPushButton()
            avatar.setStyleSheet('max-width: 70px; min-height: 70px; border: 0px; border-radius: 35px;')
            avatar.setIcon(QIcon(f"assets/img/users/{user[4]}"))
            avatar.setIconSize(QSize(70, 70))

            self.ui.gl_users.addWidget(avatar, i, 0, alignment=Qt.Alignment())
            self.ui.gl_users.addWidget(label, i, 1, alignment=Qt.Alignment())
            self.ui.gl_users.addWidget(btn, i, 2, alignment=Qt.Alignment())
            btn.clicked.connect(partial(self.deleteUser, user[0], btn, label, avatar))
        return users

    def addNewUser(self):
        AddUser(self.length)

    def deleteUser(self, id, btn, label, avatar):
        response = Database.delete(id)
        if response:
            btn.hide()
            label.hide()
            avatar.hide()
            self.msgBox("Your message deleted!")
        else:
            self.msgBox("Database error!")

    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()



class AddUser(QWidget):
    def __init__(self, len):
        super(AddUser, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('add-User.ui')
        self.ui.show()
        self.ui.btn_choose.setIcon(QIcon('assets/img/camera2.png'))
        self.ui.btn_submit.clicked.connect(self.submit)
        self.length = len
        print('self.length: ', self.length)

    def submit(self):
        name = self.ui.txt_name.text()
        nationalcode = self.ui.txt_code.text()
        birthday = self.ui.txt_birthday.text()

        if name != "" and nationalcode != "":
            response = Database.insert(name, nationalcode, birthday)
            if response:
                self.length += 1
                label = QLabel()
                label.setText(name)

                btn = QPushButton()
                btn.setText('×')
                btn.setStyleSheet('max-width: 18px; min-height: 18px; background-color: #F05454;'
                                  ' color: white; border: 0px; border-radius: 9px;')

                avatar = QPushButton()
                avatar.setStyleSheet('max-width: 70px; min-height: 70px; border: 0px; border-radius: 35px;')
                avatar.setIcon(QIcon(f"assets/img/users/user[4]"))
                avatar.setIconSize(QSize(70, 70))

                self.ui.gl_users.addWidget(avatar, self.length, 0, alignment=Qt.Alignment())
                self.ui.gl_users.addWidget(label, self.length, 1, alignment=Qt.Alignment())
                self.ui.gl_users.addWidget(btn, self.length, 2, alignment=Qt.Alignment())
                btn.clicked.connect(partial(self.deleteUser, self.length, btn, label))

                self.msgBox("User added successfully!")
            else:
                self.msgBox("Database error!")
        else:
            self.msgBox("Error: feilds are empty!")

    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec())
