import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCalendarWidget,
                             QListView, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class Planner(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("Daily Task Planner", self)

        self.calendar = QCalendarWidget(self)

        self.task_edit = QLineEdit(self)
        self.add_button = QPushButton('Add Task', self)

        self.task_view = QListView(self)
        self.model = QStandardItemModel(self)
        self.task_view.setModel(self.model)

        self.save_button = QPushButton("Save", self)

        self.data = {}

        self.date = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Notebook v2.0')
        self.resize(900, 700)

        main_layout = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        vbox1 = QVBoxLayout()

        hbox1.addWidget(self.task_edit)
        hbox1.addWidget(self.add_button)

        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.task_view)
        vbox1.addWidget(self.save_button)

        hbox2.addWidget(self.calendar)
        hbox2.addLayout(vbox1)

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(hbox2)

        self.setLayout(main_layout)

        self.title_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
                            Planner {
                                background: white;
                            }
                            QLabel {
                                font-size: 40px;
                                font-family: Courier New;
                                color: #5047D8;
                                background: white;
                                padding: 10px;
                                border: 2px solid #5047D8;
                                border-radius: 5px;
                            }
                            QLineEdit, QPushButton, QListView {
                                font-family: Courier New;
                                border: 2px solid #5047D8;
                                border-radius: 5px;
                                background: white;
                            }
                            QPushButton {
                                font-size: 15px;
                                color: #5047D8;
                                padding: 5px
                            }
                            QLineEdit {
                                color: #5047D8;
                                padding: 5px
                            }
                            QListView {
                                font-size: 18px;
                                color: #5047D8;
                                padding: 5px;
                            }
                            QCalendarWidget QWidget {
                                font-family: Courier New;
                                background-color: white;  /* White background for the calendar */
                                color: #7B72F8;
                            }
                            QCalendarWidget QAbstractItemView:enabled {
                                selection-background-color: #DFDDFF;
                                selection-color: #7B72F8;
                            }
                            QCalendarWidget QToolButton {
                                font-size: 20px
                            }
                           """)
        
        self.calendar.selectionChanged.connect(self.load_items)
        self.add_button.clicked.connect(self.add_task)
        self.save_button.clicked.connect(self.save_items)
    
    def save_items(self):
        if self.date == "":
            QMessageBox.warning(self, "Warning", "Please select a date.")
            return
        
        elif self.model.item(0).text() == "No checklist items for this date":
            QMessageBox.warning(self, "Warning", "Please add a task before saving.")
            return
        
        updated_tasks = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)

            checked = item.checkState()
            updated_tasks.append([item.text(), checked])

        self.data[self.date] = updated_tasks

        try:
            with open("data.json", "w") as file:
                json.dump(self.data, file, indent=4)

            QMessageBox.information(self, "Saved", "Successfully saved tasks!")

        except Exception as e:
            QMessageBox.critical(self, "Error" f"Error: {e}")

    def load_items(self):
        self.date = self.calendar.selectedDate().toString("yyyy-MM-dd")

        self.model.clear()

        try:
            with open("data.json", "r") as file:
                self.data = json.load(file)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Data file not found!")
            return

        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Could not decode JSON file.")

        tasks = self.data.get(self.date, [])

        if tasks:
            for task, checked in tasks:
                item = QStandardItem(task)
                item.setCheckable(True)
                item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
                self.model.appendRow(item)

        else:
            placeholder = QStandardItem("No checklist items for this date")
            placeholder.setFlags(Qt.ItemIsEnabled)  # Not checkable
            self.model.appendRow(placeholder)

    def add_task(self):
        placeholder = "No checklist items for this date"

        if self.model.item(0).text() == placeholder:
            self.model.clear()

        task = self.task_edit.text()

        if task != "":
            item = QStandardItem(task)
            item.setCheckable(True)

            self.model.appendRow(item)

            self.task_edit.clear()

        else:
            QMessageBox.warning(self, "Warning", "Cannot enter blank task.")
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    planner = Planner()
    planner.show()
    sys.exit(app.exec_())