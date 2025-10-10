import openpyxl
from tkinter import *
from tkinter import ttk

class ExcelApp:
    def __init__(self, window):
        self.window = window

        self.status_list = ['Subscribed', 'Not Subscribed', 'Others']

        self.employed = BooleanVar()

        self.file_path = 'people.xlsx'

        self.style = ttk.Style(window)
        self.window.tk.call("source", "forest-light.tcl")
        self.window.tk.call("source", "forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.style.theme_use('forest-dark')

        self.create_widgets()

        self.load_data()

    def create_widgets(self):
        self.window.title('Excel Viewer')

        self.frame = ttk.Frame(self.window)
        self.frame.pack()

        self.widget_frame = ttk.LabelFrame(self.frame, text='User Details')
        self.widget_frame.grid(row=0, column=0, padx=20, pady=10)

        self.name_entry = ttk.Entry(self.widget_frame)
        self.name_entry.insert(0, 'Name')
        self.name_entry.bind("<FocusIn>", lambda event: self.name_entry.delete(0, END))
        self.name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky='ew')

        self.age_spinbox = ttk.Spinbox(self.widget_frame, from_=18, to=100)
        self.age_spinbox.insert(0, 'Age')
        self.age_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.status_combobox = ttk.Combobox(self.widget_frame, values=self.status_list)
        self.status_combobox.current(0)
        self.status_combobox.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.employment_checkbutton = ttk.Checkbutton(self.widget_frame, text='Employed', variable=self.employed,
                                                      onvalue=True, offvalue=False)
        self.employment_checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        self.insert_button = ttk.Button(self.widget_frame, text='Insert', command=self.insert_row)
        self.insert_button.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')

        self.separator = ttk.Separator(self.widget_frame)
        self.separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky='ew')

        self.mode_button = ttk.Checkbutton(self.widget_frame, text='Mode', style='Switch', command=self.toggle_mode)
        self.mode_button.grid(row=6, column=0, padx=5, pady=10, sticky='nsew')

        self.tree_frame = ttk.LabelFrame(self.frame)
        self.tree_frame.grid(row=0, column=1, padx=(0, 20), pady=10)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side='right', fill='y', pady=5)

        cols = ('Name', 'Age', 'Subscription', 'Employment')
        self.tree_view = ttk.Treeview(self.tree_frame, show='headings', yscrollcommand=self.tree_scroll.set, columns=cols, height=13)

        self.tree_view.column('Name', width=100)
        self.tree_view.column('Age', width=50)
        self.tree_view.column('Subscription', width=100)
        self.tree_view.column('Employment', width=100)

        self.tree_view.pack(padx=(5, 0), pady=5)

        self.tree_scroll.config(command=self.tree_view.yview)

    def load_data(self):
        # Clear the tree view
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
            
        if self.file_path and self.file_path.endswith('.xlsx'):

            try:
                workbook = openpyxl.load_workbook(self.file_path)
                sheet = workbook.active

            except Exception as e:
                print(f"Error loading workbook: {e}")
                return

            list_values = list(sheet.values)
            # print(list_values)

            for col_name in list_values[0]:
                self.tree_view.heading(col_name, text=col_name)

            for value_tuple in list_values[1:]:
                self.tree_view.insert('', END, values=value_tuple)

            del workbook # optionally delete the workbook reference

    def insert_row(self):
        name = self.name_entry.get()
        age = int(self.age_spinbox.get())
        subscription_status = self.status_combobox.get()
        employment_status = 'Employed' if self.employed.get() else 'Unemployed'

        # print([name, age, subscription_status, employment_status])

        # Insert row into Excel sheet
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            sheet = workbook.active

        except Exception as e:
            print(f"Error loading workbook: {e}")
            return

        row_values = [name, age, subscription_status, employment_status]
        sheet.append(row_values)
        workbook.save(self.file_path)

        del workbook # optionally delete the workbook reference

        # Load updated Excel data
        self.load_data()

        # Clear the values
        self.name_entry.delete(0, END)
        self.name_entry.insert(0, 'Name')

        self.age_spinbox.delete(0, END)
        self.age_spinbox.insert(0, 'Age')

        self.status_combobox.set(self.status_list[0])

        self.employed.set(0)

    def toggle_mode(self):
        if self.mode_button.instate(['selected']):
            self.style.theme_use('forest-light')

        else:
            self.style.theme_use('forest-dark')

if __name__ == '__main__':
    window = Tk()
    app = ExcelApp(window)
    window.mainloop()
