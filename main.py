"""
Project: PythonProject
program: Student Management System Program
Purpose: To create and demonstrate the implementation of a SQL database and a GUI (Graphic User Interface)
         such as PyQt6 to make a fully functional student management system
Revision History:
    Created on December 27th 2024. By Juan (David) Barrios Rozo
    Edited on December 28th 2024. By Juan (David) Barrios Rozo
"""
from idlelib import statusbar

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QLayout, QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3
import funcitons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 500)

        # Menu items were included to the program
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        add_student_action.triggered.connect(self.insert)
        help_menu_item.addAction(about_action)

        # If the Help item is not shown use the following
        #about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "COURSE", "CONTACT INFO"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Implementation a toolbar and adding elements to the latter
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Integrate a status bar and a status bar elements to the program
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Adding clickable cells
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

        # Signature was integrated with the program
        signature = QLabel(funcitons.display_copyright())
        self.statusbar.addPermanentWidget(signature)
        # self.statusbar.setVisible(True)


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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Allow user to get the name/data based on the selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # Get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)

        # Dropdown box
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox

        self.course_name = QComboBox()
        courses = ["Programming Dynamic Websites", "Technology Infrastructure: Networking", "Data Modelling",
                   "Database: SQL", "Software Quality Assurance"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Implementation of the contact info widget
        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Student Contact Information")
        layout.addWidget(self.contact)

        # Submission button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                        self.contact.text(), self.student_id))

        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table
        main_window.load_data()

class DeleteDialog(QDialog):
    pass

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