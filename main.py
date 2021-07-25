# This Python file uses the following encoding: utf-8
import sys
from Database import Database
import cv2
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QSize
from PySide6 import QtGui
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
            avatar.setIcon(QtGui.QIcon(f"assets/img/users/{user[4]}"))
            avatar.setIconSize(QSize(70, 70))

            self.ui.gl_users.addWidget(avatar, i, 0, alignment=Qt.Alignment())
            self.ui.gl_users.addWidget(label, i, 1, alignment=Qt.Alignment())
            self.ui.gl_users.addWidget(btn, i, 2, alignment=Qt.Alignment())
            btn.clicked.connect(partial(self.deleteUser, user[0], btn, label, avatar))
        return users

    def addNewUser(self):
        self.add_new_user = AddUser(self.length)

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
        self.ui.btn_choose.setIcon(QtGui.QIcon('assets/img/camera2.png'))
        self.ui.btn_submit.clicked.connect(self.submit)
        self.ui.btn_choose.clicked.connect(self.takePhoto)
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

                widget.ui.gl_users.addWidget(avatar, self.length, 0, alignment=Qt.Alignment())
                widget.ui.gl_users.addWidget(label, self.length, 1, alignment=Qt.Alignment())
                widget.ui.gl_users.addWidget(btn, self.length, 2, alignment=Qt.Alignment())
                btn.clicked.connect(partial(widget.deleteUser, self.length, btn, label))

                self.msgBox("User added successfully!")
            else:
                self.msgBox("Database error!")
        else:
            self.msgBox("Error: feilds are empty!")

    def takePhoto(self):
        camera = Camera()


    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()


class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        loader = QUiLoader()
        self.ui = loader.load('filters.ui')
        self.ui.show()
        # self.ui.f1.clicked.connect(self.submit)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        video = cv2.VideoCapture(0)

        while True:
            validation, frame = video.read()
            if validation is not True:
                break

            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x, y, w, h) in faces:
                roi = frame[y:y + h, x:x + w]

            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(img)
            self.ui.f1.setIcon(QtGui.QIcon(pix))
            self.ui.f1.setIconSize(QSize(200, 200))


            cv2.imshow('output', roi)
            cv2.waitKey(30)


if __name__ == "__main__":
    app = QApplication([])
    widget = Main()
    sys.exit(app.exec())
