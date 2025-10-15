import os
import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
                             QTreeView, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()

        self.rate_label = QLabel("Interest Rate (%)", self)
        self.rate_input = QLineEdit(self)

        self.investment_label = QLabel("Initial Investment ($)", self)
        self.investment_input = QLineEdit(self)

        self.years_label = QLabel("Number of Years", self)
        self.years_input = QLineEdit(self)

        self.tree_view = QTreeView(self)
        self.model = QStandardItemModel(self)

        self.calculate_button = QPushButton("Calculate", self)
        self.clear_button = QPushButton("Clear", self)
        self.save_button = QPushButton("Save", self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.dark_mode = QCheckBox("Dark Mode", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Interest Rate Calculator")

        self.tree_view.setModel(self.model)

        main_layout = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        vbox1 = QVBoxLayout()

        hbox1.addWidget(self.rate_label)
        hbox1.addWidget(self.rate_input)
        hbox1.addWidget(self.investment_label)
        hbox1.addWidget(self.investment_input)
        hbox1.addWidget(self.years_label)
        hbox1.addWidget(self.years_input)
        hbox1.addWidget(self.dark_mode)

        vbox1.addWidget(self.tree_view)
        vbox1.addWidget(self.calculate_button)
        vbox1.addWidget(self.clear_button)
        vbox1.addWidget(self.save_button)

        hbox2.addLayout(vbox1, 30)
        hbox2.addWidget(self.canvas, 70)

        main_layout.addLayout(hbox1)
        main_layout.addLayout(hbox2)

        self.setLayout(main_layout)

        self.setStyleSheet("""
                           FinanceApp {
                               background-color: #f0f0f0;
                           }
                           QLabel, QLineEdit, QPushButton, QCheckBox {
                               background-color: #f8f8f8;
                           }
                           QTreeView {
                               background-color: #ffffff;
                           }
                           """)

        self.calculate_button.clicked.connect(self.calculate_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)
        self.dark_mode.stateChanged.connect(self.toggle_mode)

    def calculate_interest(self):
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = int(self.investment_input.text())
            num_years = int(self.years_input.text())

        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input! {e}")
            return
        
        self.model.clear()

        self.model.setHorizontalHeaderLabels(["Year", "Total"])
        
        total = initial_investment
        for year in range(1, num_years + 1):
            total += total * (interest_rate/100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem(f"$     {total:,.2f}")
            self.model.appendRow([item_year, item_total])

        self.create_graph(interest_rate, initial_investment, num_years)

    def create_graph(self, interest_rate, initial_investment, num_years):
        self.figure.clear()

        plt.style.use("seaborn-v0_8")

        ax = self.figure.subplots()
        years = list(range(1, num_years + 1))
        totals = [initial_investment * (1 + interest_rate/100) ** year for year in years]

        ax.plot(years, totals)
        ax.set_title("Growth of Investment Over Time", fontsize=24, fontweight='bold')
        ax.set_xlabel("Years of Investment", fontsize=18)
        ax.set_ylabel("Total Amount ($)", fontsize=18)

        self.canvas.draw()

    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")

        if dir_path:
            folder_path = os.path.join(dir_path, "Results")
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, "results.csv")
            with open(file_path, "w") as file:
                writer = csv.DictWriter(file, fieldnames=['Year', 'Total'])
                writer.writeheader()

                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    writer.writerow({'Year': year, 'Total': total})

            plt.savefig(f"{folder_path}/graph.png")

            QMessageBox.information(self, "Save Results", "Successfully saved to folder!")

        else:
            QMessageBox.warning(self, "Save Results", "No directory selected!")

    def reset(self):
        self.rate_input.clear()
        self.investment_input.clear()
        self.years_input.clear()
        self.model.clear()

        self.figure.clear()
        self.canvas.draw()

    def toggle_mode(self, state):
        if state == 2: # checked
            self.setStyleSheet("""
                               FinanceApp {
                                   background-color: #222222;
                               }
                               QLabel, QLineEdit, QPushButton, QCheckBox {
                                   background-color: #333333;
                                   color: #eeeeee;
                               }
                               QTreeView {
                                   background-color: #444444;
                                   color: #eeeeee;
                               }
                               """)
        else:
            self.setStyleSheet("""
                               FinanceApp {
                                   background-color: #f0f0f0;
                               }
                               QLabel, QLineEdit, QPushButton, QCheckBox {
                                   background-color: #f8f8f8;
                               }
                               QTreeView {
                                   background-color: #ffffff;
                               }
                               """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    finance_app = FinanceApp()
    finance_app.showMaximized()
    sys.exit(app.exec_())
