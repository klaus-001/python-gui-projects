import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget,
                             QPushButton, QLineEdit, QDateEdit, QComboBox,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.date_label = QLabel('Date: ', self)
        self.date_select = QDateEdit(self)
        self.category_label = QLabel('Category: ', self)
        self.category_select = QComboBox(self)

        self.amount_label = QLabel('Amount: ', self)
        self.amount_input = QLineEdit(self)
        self.description_label = QLabel('Description: ', self)
        self.description_input = QLineEdit(self)

        self.add_button = QPushButton('Add Expense', self)
        self.delete_button = QPushButton('Delete Expense', self)

        self.expense_table = QTableWidget(self)

        self.initUI()

        self.load_table()

    def initUI(self):
        self.resize(650, 600)
        self.setWindowTitle('Expense Tracker')

        self.date_select.setDate(QDate.currentDate())

        self.expense_table.setColumnCount(5) # set table column to 5
        self.expense_table.setHorizontalHeaderLabels(['Id', 'Date', 'Category', 'Amount', 'Description'])

        self.category_select.addItem('Select an option') # placeholder
        self.category_select.setCurrentIndex(0)
        self.category_select.addItems(['Personal', 'Food', 'Rent'])

        main_layout = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        hbox1.addWidget(self.date_label)
        hbox1.addWidget(self.date_select)
        hbox1.addWidget(self.category_label)
        hbox1.addWidget(self.category_select)

        hbox2.addWidget(self.amount_label)
        hbox2.addWidget(self.amount_input)
        hbox2.addWidget(self.description_label)
        hbox2.addWidget(self.description_input)

        hbox3.addWidget(self.add_button)
        hbox3.addWidget(self.delete_button)

        main_layout.addLayout(hbox1)
        main_layout.addLayout(hbox2)
        main_layout.addLayout(hbox3)
        main_layout.addWidget(self.expense_table)

        self.setLayout(main_layout)

        self.date_label.setObjectName('date_label')
        self.date_select.setObjectName('date_select')
        self.category_label.setObjectName('category_label')
        self.category_select.setObjectName('category_select')
        self.amount_label.setObjectName('amount_label')
        self.amount_input.setObjectName('amount_input')
        self.description_label.setObjectName('description_label')
        self.description_input.setObjectName('description_input')
        self.add_button.setObjectName('add_button')
        self.delete_button.setObjectName('delete_button')
        self.expense_table.setObjectName('self.expense_table')

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: tahoma;
                font-size: 15px
            }
            QDateEdit#date_select{
                font-family: tahoma;
                font-size: 15px;      
            }
            QComboBox#category_select{
                font-family: tahoma;
                font-style: italic;
                font-size: 15px;
            }
            QLineEdit#amount_input{
                font-family: tahoma;
                font-size: 15px;
            }
            QLineEdit#description_input{
                font-family: tahoma;
                font-size: 15px;
            }
            QHeaderView::section{
                font-weight: bold;
            }
        """)

        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)

    def load_table(self):
        self.expense_table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")

        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Create a new row
            self.expense_table.insertRow(row)

            # Add values to table
            self.expense_table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.expense_table.setItem(row, 1, QTableWidgetItem(date))
            self.expense_table.setItem(row, 2, QTableWidgetItem(category))
            self.expense_table.setItem(row, 3, QTableWidgetItem(f'$ {amount:,.2f}'))
            self.expense_table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        # Get the user input
        date = self.date_select.date().toString('yyyy-MM-dd')
        category = self.category_select.currentText()
        amount = self.amount_input.text()
        description = self.description_input.text()

        existing_ids = [] # list to store existing ids

        # Find smallest available id
        query = QSqlQuery("SELECT id FROM expenses ORDER BY id")
        while query.next():
            existing_ids.append(query.value(0))

        new_id = 1
        for i in range(1, (max(existing_ids) + 2) if existing_ids else 2):
            if i not in existing_ids:
                new_id = i
                break

        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (id, date, category, amount, description)
                      VALUES (?, ?, ?, ?, ?)
                      """)
        query.addBindValue(new_id)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)

        query.exec_()

        # Reset entry fields
        self.date_select.setDate(QDate.currentDate())
        self.category_select.setCurrentIndex(0)
        self.amount_input.clear()
        self.description_input.clear()

        self.load_table()

    def delete_expense(self):
        # Get the current selected row
        selected_row = self.expense_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, 'Warning!', 'Please select a row to delete!')
            return

        expense_id = int(self.expense_table.item(selected_row, 0).text())

        confirm = QMessageBox.question(self, 'Confirm?', 'Delete Expense?', QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return
            
        # Delete the selected expense
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)

        success_delete = query.exec_()

        if not success_delete:
            QMessageBox.critical(self, 'Database Error', f'Failed to delete expense: {query.lastError().text()}')
            return

        # Decrement IDs greater than the deleted id to keep ids consecutive
        query = QSqlQuery()
        query.prepare("UPDATE expenses SET id = id - 1 WHERE id > ?")
        query.addBindValue(expense_id)

        success_update = query.exec_()

        if not success_update:
            QMessageBox.critical(self, 'Database Error', f'Failed to update expense: {query.lastError().text()}')
            return

        self.load_table()


# Create database
database = QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('expense.db')

if not database.open():
    QMessageBox.critical(None, 'Database Error', 'Database could not be opened!')
    sys.exit(1) # exit with a status code of 1 to indicate an error

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    expense_tracker = ExpenseTracker()
    expense_tracker.show()
    sys.exit(app.exec_())