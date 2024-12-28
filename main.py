"""
Project: PythonProject
program: Student Management System Program
Purpose: To create and demonstrate the implementation of a SQL database and a GUI (Graphic User Interface)
         such as PyQt6 to make a fully functional student management system
Revision History:
    Created on December 27th 2024. By Juan (David) Barrios Rozo
    Edited on December 28th 2024. By Juan (David) Barrios Rozo
"""

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QLayout, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Menu items were included to the program
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        add_student_action.triggered.connect(self.insert)
        help_menu_item.addAction(about_action)

        # If the Help item is not shown use the following
        #about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name widget was added
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Dropdown box or combo box was implemented
        self.course_name = QComboBox()
        courses = ["Programming Dynamic Websites", "Technology Infrastructure: Networking", "Data Modelling",
                   "Database: SQL", "Software Quality Assurance"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Implementation of the contact info widget
        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Student Contact Information")
        layout.addWidget(self.contact)

        # Submission button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.contact.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set the window title and size
        self.setWindowTitle("Search Student Name")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Creation of the layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Implementation of the search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = list(result)
        print(row)

        items = main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1). setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())