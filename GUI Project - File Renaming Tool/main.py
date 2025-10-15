import os
import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QLabel,
                             QAction, QListView, QComboBox, QFileDialog, QWidget,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class FileRenamingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)

        self.menu_bar = self.menuBar()

        self.filter_line = QLineEdit(self)
        self.filter_button = QPushButton('Filter', self)

        self.unstage_label = QLabel('Unstaged Area:', self)
        self.stage_label = QLabel('Staged Area:', self)

        self.list_view = QListView(self)
        self.select_view = QListView(self)

        self.list_model = QStandardItemModel(self)
        self.select_model = QStandardItemModel(self)

        self.add_button = QPushButton('Stage Files', self)
        self.remove_button = QPushButton('Unstage Files', self)

        self.option_box = QComboBox(self)

        self.edit_line = QLineEdit(self)
        self.apply_button = QPushButton('Apply', self)

        # Initial directory
        self.directory = '.'

        # Empty list to store selected files
        self.selected_files = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Renaming Tool')
        self.setGeometry(500, 200, 700, 750)

        # Create menu bar
        self.file_menu = self.menu_bar.addMenu('File')

        self.open_action = QAction('Open', self)
        self.open_action.triggered.connect(self.load_directory)
        self.file_menu.addAction(self.open_action)

        # Allow multiple selection in QListView
        self.list_view.setSelectionMode(QListView.MultiSelection)
        self.select_view.setSelectionMode(QListView.MultiSelection)

        self.list_view.setModel(self.list_model)
        self.select_view.setModel(self.select_model)

        # Add items to combo box
        self.option_box.addItem('Select an option') # set placeholder
        self.option_box.setCurrentIndex(0)
        self.option_box.addItems(['Add Prefix', 'Remove Prefix', 'Add Suffix', 'Remove Suffix', 'Rename'])

        # Create a central widget
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox2= QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        hbox1.addWidget(self.filter_line)
        hbox1.addWidget(self.filter_button)

        hbox2.addWidget(self.stage_label, 80)
        hbox2.addWidget(self.option_box, 20)

        hbox3.addWidget(self.add_button)
        hbox3.addWidget(self.remove_button)

        hbox4.addWidget(self.edit_line)
        hbox4.addWidget(self.apply_button)

        main_layout.addLayout(hbox1)
        main_layout.addLayout(hbox2)
        main_layout.addWidget(self.select_view)
        main_layout.addWidget(self.unstage_label)
        main_layout.addWidget(self.list_view)
        main_layout.addLayout(hbox3)
        main_layout.addLayout(hbox4)

        self.central_widget.setLayout(main_layout)

        self.filter_button.clicked.connect(self.filter_selection)
        self.add_button.clicked.connect(self.add_selection)
        self.remove_button.clicked.connect(self.remove_selection)
        self.apply_button.clicked.connect(self.rename_files)

    def load_directory(self):
        try:
            self.directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
            
            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.list_model.appendRow(QStandardItem(file))

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not load directory: {e}')
            return 

    def filter_selection(self):
        self.select_model.clear()

        self.selected_files = []

        for index in range(self.list_model.rowCount()):
            item = self.list_model.item(index)

            # Use regex to find any files that contains the suggestion in the directory
            if re.match(self.filter_line.text(), item.text()): # use: .*sample.*
                self.select_model.appendRow(QStandardItem(item.text()))
                self.selected_files.append(item.text())

            # allow direct search 
            elif self.filter_line.text() == item.text():
                self.select_model.appendRow(QStandardItem(item.text()))
                self.selected_files.append(item.text())

    def add_selection(self):
        if len(self.list_view.selectedIndexes()) != 0:

            for index in self.list_view.selectedIndexes():

                if index.data() not in self.selected_files:

                    self.selected_files.append(index.data())
                    self.select_model.appendRow(QStandardItem(index.data()))

    def remove_selection(self):
        try:
            if len(self.select_view.selectedIndexes()) != 0:
                # reversed to allow safe removal of items
                for index in reversed(sorted(self.select_view.selectedIndexes())):
                    self.selected_files.remove(index.data())
                    self.select_model.removeRow(index.row())

        except Exception as e:
            QMessageBox.critical(self, 'Unstaging Error', f'Could not unstage files: {e}')
            return

    def rename_files(self):
        # Get user input
        option = self.option_box.currentText()
        new_text = self.edit_line.text()

        counter = 1

        # Edit filename based on which option is selected
        for filename in self.selected_files:
            if option == 'Add Prefix':
                os.rename(os.path.join(self.directory, filename),
                os.path.join(self.directory, f'{new_text}{filename}'))

            elif option == 'Remove Prefix':
                if filename.startswith(new_text):
                    os.rename(os.path.join(self.directory, filename),
                    os.path.join(self.directory, filename[len(new_text):]))

            elif option == 'Add Suffix':
                filetype = filename.split('.')[-1]

                os.rename(os.path.join(self.directory, filename),
                os.path.join(self.directory, f'{filename[:-(len(filetype) + 1)]}{new_text}.{filetype}'))

            elif option == 'Remove Suffix':
                filetype = filename.split('.')[-1]

                if filename.endswith(f'{new_text}.{filetype}'):
                    os.rename(os.path.join(self.directory, filename),
                    os.path.join(self.directory, f'{filename[:-len(new_text + '.' + filetype)]}.{filetype}'))

            elif option == 'Rename':
                filetype = filename.split('.')[-1]

                os.rename(os.path.join(self.directory, filename),
                os.path.join(self.directory, f'{new_text}{counter}.{filetype}'))

                counter += 1

            else:
                QMessageBox.warning(self, 'Warning', 'Select an edit option!')
                return

            # Empty the list, clear the models, and reset option box
            self.selected_files = []
            self.select_model.clear()
            self.list_model.clear()
            self.edit_line.clear()
            self.option_box.setCurrentIndex(0)

            # Show the updated filenames 
            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.list_model.appendRow(QStandardItem(file))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = FileRenamingTool()
    tool.show()
    sys.exit(app.exec_())