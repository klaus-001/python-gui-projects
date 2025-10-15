import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QComboBox,
                             QTreeView, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from docxtpl import DocxTemplate
from docx2pdf import convert

class InvoiceGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.firstname_label = QLabel('First Name: ', self)
        self.firstname_edit = QLineEdit(self)
        self.lastname_label = QLabel('Last Name: ', self)
        self.lastname_edit = QLineEdit(self)
        self.phone_label = QLabel('Phone: ', self)
        self.phone_edit = QLineEdit(self)
        self.qty_label = QLabel('Qty: ', self)
        self.qty_spinbox = QSpinBox(self)
        self.description_label = QLabel('Description: ', self)
        self.description_combobox = QComboBox(self)
        self.price_label = QLabel('Unit Price: ', self)
        self.price_edit = QLineEdit(self)
        self.add_button = QPushButton('Add Item', self)
        self.tree_view = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.generate_button = QPushButton('Generate Invoice', self)
        self.new_button = QPushButton('New Invoice', self)
        self.remove_button = QPushButton('Remove Item', self)

        self.invoice_list = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Invoice Generator')

        # Add items to combo box
        # Change base on what items the user offers
        self.description_combobox.addItem(' -- Select an item description -- ')
        self.description_combobox.setCurrentIndex(0)
        self.description_combobox.addItems(['Plywood', '40x40 I-beam', 'Rivets', 'Hollow Blocks'])

        self.tree_view.setSelectionMode(QAbstractItemView.MultiSelection) # allow multiple selection

        self.tree_view.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Qty', 'Description', 'Unit Price', 'Total'])

        self.tree_view.setIndentation(0) # removes indentation showing hierarchy between headers and rows

        self.tree_view.setColumnWidth(0, 200)
        self.tree_view.setColumnWidth(1, 200)
        self.tree_view.setColumnWidth(2, 200)
        self.tree_view.setColumnWidth(3, 200)

        main_layout = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        
        vbox1= QVBoxLayout()
        vbox2 = QVBoxLayout()

        hbox1.addWidget(self.firstname_label)
        hbox1.addWidget(self.firstname_edit)

        hbox2.addWidget(self.lastname_label)
        hbox2.addWidget(self.lastname_edit)

        hbox3.addWidget(self.phone_label)
        hbox3.addWidget(self.phone_edit)

        hbox4.addWidget(self.qty_label)
        hbox4.addWidget(self.qty_spinbox)

        hbox5.addWidget(self.description_label)
        hbox5.addWidget(self.description_combobox)

        hbox6.addWidget(self.price_label)
        hbox6.addWidget(self.price_edit)

        hbox7.addWidget(self.add_button)
        hbox7.addWidget(self.remove_button)

        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        vbox2.addLayout(hbox4)
        vbox2.addLayout(hbox5)
        vbox2.addLayout(hbox6)
        vbox2.addLayout(hbox7)

        hbox8.addLayout(vbox1)
        hbox8.addLayout(vbox2)

        main_layout.addLayout(hbox8)
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(self.generate_button)
        main_layout.addWidget(self.new_button)

        self.setLayout(main_layout)

        self.generate_button.clicked.connect(self.generate_invoice)
        self.new_button.clicked.connect(self.new_invoice)
        self.add_button.clicked.connect(self.add_items)
        self.remove_button.clicked.connect(self.remove_items)

        self.resize(800, 500)

    def add_items(self):
        try:
            qty = int(self.qty_spinbox.text())
            description = self.description_combobox.currentText()
            unit_price = float(self.price_edit.text())
            total = qty * unit_price

        except ValueError as e:
            QMessageBox.critical(self, 'Value Error', f'Error: {e}')
            return
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {e}')
            return

        qty_item = QStandardItem(str(qty))
        desc_item = QStandardItem(description)
        unit_price_item = QStandardItem(f'{unit_price:.2f}')
        total_item = QStandardItem(f'{total:.2f}')

        self.model.appendRow([qty_item, desc_item, unit_price_item, total_item])

        self.qty_spinbox.setValue(0)
        self.description_combobox.setCurrentIndex(0)
        self.price_edit.clear()

    def remove_items(self):
        try:
            selected_indexes = self.tree_view.selectedIndexes()
            if selected_indexes:
                # Get unique rows from selected indexes to avoid removing the same row multiple times
                rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
                for row in rows:
                    self.model.removeRow(row)
            else:
                QMessageBox.warning(self, 'Warning', "No items selected for removal.")

        except Exception as e:
            QMessageBox.critical(self, 'Removal Error', f'Could not remove items: {e}')

    def generate_invoice(self):
        first_name = self.firstname_edit.text()
        last_name = self.lastname_edit.text()
        name = f'{first_name} {last_name}'
        phone = self.phone_edit.text()

        subtotal = 0

        if last_name == '' or self.model.rowCount() == 0:
            return

        for row in range(self.model.rowCount()):
            qty = int(self.model.index(row, 0).data())
            description = self.model.index(row, 1).data()
            unit_price = float(self.model.index(row, 2).data())
            unit_total = float(self.model.index(row, 3).data())
            subtotal += unit_total

            unit_price = f'$ {unit_price:.2f}'
            unit_total = f'$ {unit_total:.2f}'

            self.invoice_list.append([qty, description, unit_price, unit_total])

        sales_tax = 0.12
        overall_total = subtotal * (1 + sales_tax)

        doc = DocxTemplate('invoice_template.docx')
        doc.render(
            {
                'name': name,
                'phone': phone,
                'invoice_list': self.invoice_list,
                'subtotal': f'$ {subtotal:.2f}',
                'salestax': f'{sales_tax * 100:.0f} %',
                'total': f'$ {overall_total:.2f}'
            }
        )

        filename = f'Invoice_{last_name}_{datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")}'
        doc_name = filename + '.docx'
        doc.save(doc_name)

        InvoiceGenerator.doc_to_pdf(filename, doc_name)

        self.new_invoice()

        QMessageBox.information(self, 'Success', 'Invoice has been successfully generated.')

    def new_invoice(self):
        self.firstname_edit.clear()
        self.lastname_edit.clear()
        self.phone_edit.clear()

        self.qty_spinbox.setValue(0)
        self.description_combobox.setCurrentIndex(0)
        self.price_edit.clear()

        # Clear model and reset tree view config
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Qty', 'Description', 'Unit Price', 'Total'])
        self.tree_view.setColumnWidth(0, 200)
        self.tree_view.setColumnWidth(1, 200)
        self.tree_view.setColumnWidth(2, 200)
        self.tree_view.setColumnWidth(3, 200)

        self.invoice_list = [] # set to empty list

    @staticmethod
    def doc_to_pdf(filename, doc_file):
        try:
            convert(doc_file, filename + '.pdf')

        except Exception as e:
            QMessageBox.critical(None, 'Error', 'Error converting docx to pdf!')
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    invoice = InvoiceGenerator()
    invoice.show()
    sys.exit(app.exec_())