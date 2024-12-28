"""
Project: PythonProject
program: Student Management System Program
Purpose: To create and demonstrate the implementation of a SQL database and a GUI (Graphic User Interface)
         such as PyQt6 to make a fully functional student management system
Revision History:
    Created on December 27th 2024. By Juan (David) Barrios Rozo
    Edited on December 28th 2024. By Juan (David) Barrios Rozo
"""
from idlelib.debugger_r import close_subprocess_debugger

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QLayout, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        add_student_action.triggered.connect(self.insert)
        help_menu_item.addAction(about_action)

        # If the Help item is not shown use the following
        #about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "CONTACT INFO"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        results = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name widget was added
        student_name = QLineEdit()
        student_name.setPlaceholderText("Student Name")
        layout.addWidget(student_name)

        # Dropdown box or combo box was implemented
        course_name = QComboBox()
        courses = ["Programming Dynamic Websites", "Technology Infrastructure: Networking", "Data Modelling", "Database: SQL", "Software Quality Assurance"]
        course_name.addItem(courses)
        layout.addWidget(course_name)


        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())