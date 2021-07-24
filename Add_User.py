from PySide6.QtGui import QIcon

from Database import Database
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from functools import partial
from datetime import datetime


class AddUser(QWidget):

    def __init__(self):
        super(AddUser, self).__init__()


    @staticmethod
    def addNewUser():
        loader = QUiLoader()
        ui = loader.load('add-User.ui')
        ui.show()
        ui.btn_choose.setIcon(QIcon('assets/img/camera2.png'))

        name = ui.txt_name.text()
        text = ui.txt_message.text()
        now = datetime.now().strftime('%H')

        if name != "" and text != "":
            for message in AddUser.messages:
                if name == message[1]:
                    if int(now) - int(message[3][11:12]) <= 0:
                        AddUser.msgBox("Your message should be for 1 hour ago or more")
                        break
            else:
                response = Database.insert(name, text)
                if response:
                    AddUser.length += 1
                    label = QLabel()
                    label.setText(name + ": " + text)
                    AddUser.ui.gl_messages.addWidget(label, AddUser.length, 1, alignment=Qt.Alignment())

                    btn = QPushButton()
                    btn.setText('×')
                    btn.setStyleSheet(
                        'max-width: 18px; min-height: 18px; background-color: red; '
                        'color: white; border: 0px; border-radius: 5px;')
                    ui.gl_messages.addWidget(btn, AddUser.length, 0, alignment=Qt.Alignment())
                    btn.clicked.connect(partial(AddUser.deleteMessage, AddUser.messages[-1][0], btn, label))

                    ui.txt_name.setText("")
                    ui.txt_message.setText("")

                    AddUser.msgBox("Your message sent successfully!")
                else:
                    AddUser.msgBox("Database error!")
        else:
            AddUser.msgBox("Error: feilds are empty!")

    def msgBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec_()

