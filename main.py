import database
from functools import partial
import sys
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui",None)
        self.ui.show()
        self.ui.btn_add.clicked.connect(self.add)
        self.ui.exit.triggered.connect(exit)
        self.ui.help.triggered.connect(self.info)
        self.flag = 0
        self.read_from_Database()

    def read_from_Database(self):
        result = database.select()
        for i in range(len(result)):
            self.label = QLabel()
            self.buttom = QPushButton()
            self.checkbox = QCheckBox()
            self.delete_btn = QPushButton()
            self.btn_mark = QPushButton()

            self.btn_mark.setStyleSheet("background-image : url(img/mark.png);max-width: 24px; min-height: 24px;border-radius:12px;background-color:rgb(120, 249, 81);")
            self.label.setText(result[i][1])
            self.buttom.setStyleSheet("background-image : url(img/detail.png);max-width: 24px; min-height: 24px;background-color:#f7ff58;border-radius:12px;")
            self.delete_btn.setStyleSheet("background-image : url(img/delete.png);max-width: 24px; min-height: 24px;border-radius:12px;background-color: #ff6978")
            if result[i][6] == 1:
                self.label.setStyleSheet('color: red;font: 700 11pt "Segoe UI";')
            else:self.label.setStyleSheet('color: rgb(0, 114, 187);font: 700 11pt "Segoe UI";')

            if self.flag == 0:
                if result[i][3] ==1:
                    self.ui.gridLayout1.addWidget(self.delete_btn,i,0)
                    self.delete_btn.clicked.connect(partial(self.delete,result[i],self.label,self.checkbox,self.buttom,self.delete_btn,self.btn_mark))
                    self.ui.gridLayout1.addWidget(self.label,i,2)
                    self.ui.gridLayout1.addWidget(self.buttom,i,1)
                    self.buttom.clicked.connect(partial(self.information,result[i]))
                    self.ui.gridLayout1.addWidget(self.checkbox,i,3)
                    self.checkbox.setChecked(True)
                    self.checkbox.setDisabled(True)
                else:
                    self.ui.gridLayout.addWidget(self.delete_btn,i,1)
                    self.ui.gridLayout.addWidget(self.btn_mark,i,0)
                    self.delete_btn.clicked.connect(partial(self.delete,result[i],self.label,self.checkbox,self.buttom,self.delete_btn,self.btn_mark))
                    self.btn_mark.clicked.connect(partial(self.mark,result[i],self.label,self.checkbox,self.buttom,self.delete_btn,self.btn_mark))
                    self.ui.gridLayout.addWidget(self.label,i,3)
                    self.ui.gridLayout.addWidget(self.buttom,i,2)
                    self.buttom.clicked.connect(partial(self.information,result[i]))
                    self.ui.gridLayout.addWidget(self.checkbox,i,4)

            elif self.flag == 1:
                if result[i][3] ==1:
                    self.ui.gridLayout1.addWidget(self.delete_btn,i,0)
                    self.delete_btn.clicked.connect(partial(self.delete,result[i],self.label,self.checkbox,self.buttom,self.delete_btn,self.btn_mark))
                    self.ui.gridLayout1.addWidget(self.label,i,2)
                    self.ui.gridLayout1.addWidget(self.buttom,i,1)
                    self.buttom.clicked.connect(partial(self.information,result[i]))
                    self.ui.gridLayout1.addWidget(self.checkbox,i,3)
                    self.checkbox.setChecked(True)
                    self.checkbox.setDisabled(True)

    def information(self,i):
        msg = QMessageBox()
        msg.setText("Information")
        msg.setInformativeText(f"Tile: {i[1]}\nDescription: {i[2]}\nDate: {i[4]}\nTime: {i[5]}")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def mark(self,i,label,checkbox,btn,btn_del,btn_mark):
        if checkbox.isChecked():
            self.flag = 1
            database.mark(i[1])
            self.read_from_Database()
            label.deleteLater()
            checkbox.deleteLater()
            btn.deleteLater()
            btn_del.deleteLater()
            btn_mark.deleteLater()
            self.flag = 0
                    
    def delete(self,i,label,checkbox,btn,btn_del,btn_mark):
        database.delete(i[1])
        label.deleteLater()
        checkbox.deleteLater()
        btn.deleteLater()
        btn_del.deleteLater()
        btn_mark.deleteLater()
        msg = QMessageBox()
        msg.setText("Delete")
        msg.setInformativeText("Your Task has been deleted")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def info(self):
        msg = QMessageBox()
        msg.setText("ToDoList")
        msg.setInformativeText("GUI ToDoList using Pyside6\nThis program was developed by Alireza Kiaeipour\nContact developer: a.kiaipoor@gmail.com\nBuilt in 2021")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def add(self):
        self.ui = Add()

class Add(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("form_add.ui",None)
        self.ui.show()
        self.ui.back.clicked.connect(self.back)
        self.ui.added.clicked.connect(self.add_to_Database)
    
    def back(self):
        self.ui = Main()

    def add_to_Database(self):
        title = self.ui.title.text()
        description = self.ui.description.text()
        date = self.ui.date.text()
        time = self.ui.time.text()
        if self.ui.comboBox.currentText() =="Important":
            important = 1
        elif self.ui.comboBox.currentText() =="non-Important":
            important = 0
        if title =="":
            msg = QMessageBox()
            msg.setText("Title empty")
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
        else:database.add(title,description,date,time,important)
        self.ui.title.setText("")
        self.ui.description.setText("")
        self.ui.date.setText("")
        self.ui.time.setText("")
        
app = QApplication(sys.argv)
window = Main()
app.exec()
