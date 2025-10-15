import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDateEdit, QLabel, QLineEdit, QCheckBox,
QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QHeaderView, QMessageBox)
from PyQt5.QtCore import QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class FitnessTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.button_click()

    def settings(self):
        self.setWindowTitle('Fitness Tracker')
        self.setFixedSize(800, 600)

    def initUI(self):
        self.date_label = QLabel('Date:', self)
        self.date_box = QDateEdit(self)
        self.date_box.setDate(QDate.currentDate())

        self.cal_label = QLabel('Cal:', self)
        self.cal_edit = QLineEdit(self)
        self.cal_edit.setPlaceholderText('Number of Burned Calories')

        self.km_label = QLabel('KM:', self)
        self.km_edit = QLineEdit(self)
        self.km_edit.setPlaceholderText('Enter distance ran')

        self.description_label = QLabel('Des:', self)
        self.description_edit = QLineEdit(self)
        self.description_edit.setPlaceholderText('Enter a description')

        self.dark_mode = QCheckBox('Dark Mode', self)

        self.add_btn = QPushButton('Add', self)
        self.del_btn = QPushButton('Delete', self)

        self.submit_btn = QPushButton('Submit', self)
        self.clear_btn = QPushButton('Clear', self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Calories', 'Distance', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        main_layout = QHBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()

        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        row1.addWidget(self.date_label)
        row1.addWidget(self.date_box)

        row2.addWidget(self.cal_label)
        row2.addWidget(self.cal_edit)

        row3.addWidget(self.km_label)
        row3.addWidget(self.km_edit)

        row4.addWidget(self.description_label)
        row4.addWidget(self.description_edit)

        row5.addWidget(self.add_btn)
        row5.addWidget(self.del_btn)

        row6.addWidget(self.submit_btn)
        row6.addWidget(self.clear_btn)

        col1.addLayout(row1)
        col1.addLayout(row2)
        col1.addLayout(row3)
        col1.addLayout(row4)
        col1.addWidget(self.dark_mode)
        col1.addLayout(row5)
        col1.addLayout(row6)

        col2.addWidget(self.canvas)
        col2.addWidget(self.table)

        main_layout.addLayout(col1, 30)
        main_layout.addLayout(col2, 70)

        self.setLayout(main_layout)

        self.apply_styles()
        self.load_table()

    def button_click(self):
        self.add_btn.clicked.connect(self.add_workout)
        self.del_btn.clicked.connect(self.delete_workout)
        self.submit_btn.clicked.connect(self.calculate_calories)
        self.clear_btn.clicked.connect(self.reset)
        self.dark_mode.stateChanged.connect(self.toggle_dark)

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM data ORDER BY date DESC")
        row = 0

        while query.next():
            fit_id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(fit_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.cal_edit.text()
        distance = self.km_edit.text()
        description = self.description_edit.text()

        query = QSqlQuery("""
                          INSERT INTO data (date, calories, distance, description)
                          VALUES (?, ?, ?, ?)
                          """)
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.exec_()

        self.date_box.setDate(QDate.currentDate())
        self.cal_edit.clear()
        self.km_edit.clear()
        self.description_edit.clear()

        self.load_table()

    def delete_workout(self):
        selected_row = self.table.currentRow()

        if selected_row == -1: # no row selected
            QMessageBox.warning(self, 'Warning!', 'Please choose a row to delete')
            return

        fit_id = int(self.table.item(selected_row, 0).text())

        confirm = QMessageBox.question(self, "Confirmation", "Delete this workout?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM data WHERE id = ?")
        query.addBindValue(fit_id)

        query.exec_()

        self.load_table()

    def calculate_calories(self):
        distances = []
        calories = []

        query = QSqlQuery("SELECT distance, calories FROM data ORDER BY calories ASC")

        while query.next():
            distance = query.value(0)
            calorie = query.value(1)
            distances.append(distance)
            calories.append(calorie)

        try:
            self.figure.clear()

            min_calorie = min(calories)
            max_calorie = max(calories)

            normalized_calories = [(calorie - min_calorie) / (max_calorie - min_calorie) for calorie in calories]

            plt.style.use("Solarize_Light2")
            ax = self.figure.subplots()
            ax.scatter(distances, calories, c=normalized_calories, cmap='viridis', label='Data Points')
            ax.set_title("Distance Vs. Calories")
            ax.set_xlabel("Distance")
            ax.set_ylabel("Calories")
            cbar = ax.figure.colorbar(ax.collections[0], label='Normalized Calories')
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.warning(self, "Error", "Please enter some data first!")

    def apply_styles(self):
        self.setStyleSheet("""
                           QWidget {
                               background-color: #b8c9e1;
                           }
                           QLabel {
                               color: #333;
                               font-size: 14px;
                           }
                           QLineEdit, QCheckBox, QDateEdit, QPushButton {
                               background-color: #b8c9e1;
                               color: #333;
                               border: 1px solid #444;
                               padding: 5px;
                           }
                           QTableWidget {
                               background-color: #b8c9e1;
                               color: #333;
                               border: 1px solid #444;
                               selection-background-color: #ddd;
                           }
                           QPushButton {
                               background-color: #4caf50;
                               color: #fff;
                               border: none;
                               padding: 8px 16px;
                               font-size: 14px
                           }
                           QPushButton:hover {
                               background-color: #45a049;
                           }
                           QHeaderView::section {
                               background-color: #b8c9e1;
                               color: #ffffff;
                           }
                           """)
        figure_color = '#b8c9e1'
        self.figure.patch.set_facecolor(figure_color)
        self.canvas.setStyleSheet(f"background-color: {figure_color}")
        self.canvas.draw()

        if self.dark_mode.isChecked():
            self.setStyleSheet("""
                               QWidget {
                                   background-color: #222222;
                               }
                               QLabel {
                                   color: #ffffff;
                                   font-size: 14px;
                               }
                               QLineEdit, QCheckBox, QDateEdit, QPushButton {
                                   background-color: #222222;
                                   color: #ffffff;
                                   border: 1px solid #444;
                                   padding: 5px;
                               }
                               QTableWidget {
                                   background-color: #222222;
                                   color: #ffffff;
                                   border: 1px solid #444;
                                   selection-background-color: #ddd;
                               }
                               QPushButton {
                                   background-color: #40484c;
                                   color: #fff;
                                   border: none;
                                   padding: 8px 16px;
                                   font-size: 14px
                               }
                               QPushButton:hover {
                                   background-color: #444d4f;
                               }
                               QHeaderView::section {
                                   background-color: #333333;
                                   color: #ffffff;
                               }
                               """)
            
            figure_color = '#222222'
            self.figure.patch.set_facecolor(figure_color)
            self.canvas.setStyleSheet(f"background-color: {figure_color}")
            self.canvas.draw()

    def toggle_dark(self):
        self.apply_styles()

    def reset(self):
        self.date_box.setDate(QDate.currentDate())
        self.cal_edit.clear()
        self.km_edit.clear()
        self.description_edit.clear()
        self.figure.clear()
        self.canvas.draw()

# Create database
database = QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('fitness.db')

if not database.open():
    QMessageBox.critical(None, 'Database Error', 'Database could not be opened!')
    sys.exit(1)

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                calories REAL,
                distance REAL,
                description TEXT
            )
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fitness_tracker = FitnessTracker()
    fitness_tracker.show()
    sys.exit(app.exec_())