import sv_ttk
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from nationality import nationalities

class Form:
    def __init__(self, window):
        self.window = window

        sv_ttk.set_theme('dark')

        self.salutations = ['Mr.', 'Mrs.', 'Ms.']

        self.nationalities = nationalities

        self.registered = BooleanVar()
        self.terms_co = BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        self.window.title("User Details")

        self.frame = ttk.Frame(self.window)
        self.frame.pack()

        self.label_frame = ttk.LabelFrame(self.frame, text="User Information", padding=5)
        self.label_frame.grid(row=0, column=0, padx=20, pady=20)

        self.firstName_label = ttk.Label(self.label_frame, text="First Name")
        self.firstName_label.grid(row=0, column=0)

        self.lastName_label = ttk.Label(self.label_frame, text="Last Name")
        self.lastName_label.grid(row=0, column=1)

        self.title_label = ttk.Label(self.label_frame, text="Title")
        self.title_label.grid(row=0, column=2)

        self.firstName_entry = ttk.Entry(self.label_frame)
        self.firstName_entry.grid(row=1, column=0)

        self.lastName_entry = ttk.Entry(self.label_frame)
        self.lastName_entry.grid(row=1, column=1)

        self.salutations_box = ttk.Combobox(self.label_frame, values=self.salutations)
        self.salutations_box.set("Select an option")
        self.salutations_box.grid(row=1, column=2)

        self.age_label = ttk.Label(self.label_frame, text="Age")
        self.age_label.grid(row=2, column=0)

        self.nationality_label = ttk.Label(self.label_frame, text="Nationality")
        self.nationality_label.grid(row=2, column=1)

        self.age_box = ttk.Spinbox(self.label_frame, from_=18, to=100, increment=1, wrap=True)
        self.age_box.grid(row=3, column=0)
        self.age_box.bind("<Key>", self.disable_typing)

        self.nationality_box = ttk.Combobox(self.label_frame, values=self.nationalities)
        self.nationality_box.grid(row=3, column=1)
        self.nationality_box.bind("<Key>", self.disable_typing)

        for widget in self.label_frame.winfo_children():
            widget.grid_configure(padx=20, pady=5)

        self.label_frame2 = ttk.LabelFrame(self.frame, padding=5)
        self.label_frame2.grid(row=1, column=0, sticky="news", padx=20, pady=20)

        self.registration_label = ttk.Label(self.label_frame2, text="Registration Status")
        self.registration_label.grid(row=0, column=0)

        self.course_label = ttk.Label(self.label_frame2, text="# Course Completed")
        self.course_label.grid(row=0, column=1)

        self.semesters_label = ttk.Label(self.label_frame2, text="# Semesters")
        self.semesters_label.grid(row=0, column=2)

        self.registration_box = ttk.Checkbutton(self.label_frame2, text="Currently Registered",
                                            variable=self.registered, onvalue=True, offvalue=False)
        self.registration_box.grid(row=1, column=0)

        self.course_box = ttk.Spinbox(self.label_frame2, from_=0, to='infinity')
        self.course_box.grid(row=1, column=1)
        self.course_box.bind("<Key>", self.disable_typing)

        self.semesters_box = ttk.Spinbox(self.label_frame2, from_=0, to='infinity')
        self.semesters_box.grid(row=1, column=2)
        self.semesters_box.bind("<Key>", self.disable_typing)

        for widget in self.label_frame2.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        self.label_frame3 = ttk.LabelFrame(self.frame, text="Terms & Conditions", padding=5)
        self.label_frame3.grid(row=2, column=0, sticky="news", padx=20, pady=20)

        self.terms_box = ttk.Checkbutton(self.label_frame3, text="I accept the terms and condtions.",
                                     variable=self.terms_co, onvalue=True, offvalue=False)
        self.terms_box.grid(row=0, column=0, padx=10, pady=5)

        self.enter_button = ttk.Button(self.frame, text="Enter Data", command=self.get_data)
        self.enter_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    def get_data(self):
        # Checks if the terms and conditions have been checked
        if not self.terms_co.get():
            messagebox.showwarning("Warning", "Please accept the terms and conditions!")
            return

        # Get the details 
        first_name = self.firstName_entry.get()
        last_name = self.lastName_entry.get()
        salutations = self.salutations_box.get()
        age = self.age_box.get()
        nationality = self.nationality_box.get()
        num_courses = self.course_box.get()
        num_semesters = self.semesters_box.get()

        if self.registered.get():
            registered = "Yes"
        else:
            registered = "No"

        # Checks if required fields have been filled
        if first_name == "" or last_name == "" or salutations == "" or nationality == "":
            messagebox.showwarning("Warning", "Please fill up all required fields!")
            return

        # Insert the details into the database
        conn = sqlite3.connect('users_info.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users\
                       (firstname, lastname, salutations, age, nationality, courses, semesters, registered)\
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (first_name, last_name, salutations, age, nationality, num_courses, num_semesters, registered ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Successful", "User information has been successfully added!")

        self.reset_fields()
    
    def reset_fields(self):
        self.firstName_entry.delete(0, END)
        self.lastName_entry.delete(0, END)

        self.salutations_box.delete(0, END)
        self.salutations_box.set("Select an option")

        self.age_box.delete(0, END)
        self.age_box.insert(0, 18)

        self.nationality_box.delete(0, END)

        self.course_box.delete(0, END)
        self.course_box.insert(0, 0)

        self.semesters_box.delete(0, END)
        self.semesters_box.insert(0, 0)

        self.registered.set(0)

        self.terms_co.set(0)

    def disable_typing(self, event):
        return "break"

# Create database
conn = sqlite3.connect('users_info.db') # connect to the database
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   firstname TEXT NOT NULL,
                   lastname TEXT NOT NULL,
                   salutations TEXT NOT NULL,
                   age INTEGER NOT NULL,
                   nationality TEXT NOT NULL,
                   courses INTEGER NOT NULL,
                   semesters INTEGR NOT NULL,
                   registered TEXT NOT NULL
               )
               """)
conn.commit()
conn.close()

if __name__ == '__main__':
    window = Tk()
    form = Form(window)
    window.mainloop()