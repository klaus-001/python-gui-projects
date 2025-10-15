import random
import os
import win32api
import threading
import smtplib
import sqlite3
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox

root = Tk()
root.geometry("1270x745+150+22")
root.title("Retail Billing System")
root.resizable(False, False)

def init_db():
    conn = sqlite3.connect("sales_orders.db")
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS bills (
                       bill_id TEXT,
                       name TEXT,
                       phone TEXT,
                       cosmetic_price TEXT,
                       cosmetic_tax TEXT,
                       grocery_price TEXT,
                       grocery_tax TEXT,
                       drink_price TEXT,
                       drink_tax TEXT,
                       receipt TEXT
                   )
                   """)
    
    conn.commit()
    conn.close()

def insert_row(query, params):
    conn = sqlite3.connect("sales_orders.db")
    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()
    conn.close()

class RBS:
    def __init__(self, root):
        self.root = root

        self.bill_number = 0
        self.total_cost = 0

        self.create_widgets()

    def create_widgets(self):
        self.heading_lb = Label(self.root, text="Retail Billing System", font=("Arial", 30, "bold"), bg="#df6b1e",
                                fg="gray20", bd=12, relief=GROOVE, pady=10)
        self.heading_lb.pack(fill=X)

        self.customer_details_fm = LabelFrame(self.root, text="Customer Details", font=("Arial", 15, "bold"),
                                              bg="#df6b1e", fg="gray20", bd=8, relief=GROOVE)

        self.name_lb = Label(self.customer_details_fm, text="Name", font=("Arial", 13, "bold"), bg="#df6b1e",
                             fg="white")
        self.name_lb.grid(row=0, column=0)

        self.name_ent = Entry(self.customer_details_fm, font=("Arial", 15, "bold"), bd=7, relief=GROOVE)
        self.name_ent.grid(row=0, column=1)

        self.phone_lb = Label(self.customer_details_fm, text="Phone", font=("Arial", 13, "bold"), bg="#df6b1e",
                              fg="white")
        self.phone_lb.grid(row=0, column=2)

        self.phone_ent = Entry(self.customer_details_fm, font=("Arial", 15, "bold"), bd=7, relief=GROOVE)
        self.phone_ent.grid(row=0, column=3)

        self.bill_lb = Label(self.customer_details_fm, text="Bill No.", font=("Arial", 13, "bold"), bg="#df6b1e",
                             fg="white")
        self.bill_lb.grid(row=0, column=4)

        self.bill_ent = Entry(self.customer_details_fm, font=("Arial", 15, "bold"), bd=7, relief=GROOVE)
        self.bill_ent.grid(row=0, column=5)

        self.search_btn = Button(self.customer_details_fm, text="SEARCH", font=("Arial", 12, "bold"), bd=7,
                                 command=self.search_bill)
        self.search_btn.grid(row=0, column=6)

        self.customer_details_fm.pack(fill=X, pady=(8, 0))

        for widget in self.customer_details_fm.winfo_children():
            widget.grid_configure(padx=20, pady=8)

        self.products_fm = Frame(self.root)

        self.cosmetics_fm = LabelFrame(self.products_fm, text="Cosmetics", font=("Arial", 15, "bold"), bg="#df6b1e",
                                       fg="gray20", bd=8, relief=GROOVE)
        
        self.bath_soap_lb = Label(self.cosmetics_fm, text="Bath Soap", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.bath_soap_lb.grid(row=0, column=0, sticky="w")

        self.bath_soap_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.bath_soap_ent.grid(row=0, column=1)
        self.bath_soap_ent.insert(0, 0)

        self.face_cream_lb = Label(self.cosmetics_fm, text="Face Cream", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.face_cream_lb.grid(row=1, column=0, sticky="w")

        self.face_cream_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.face_cream_ent.grid(row=1, column=1)
        self.face_cream_ent.insert(0, 0)

        self.face_wash_lb = Label(self.cosmetics_fm, text="Face Wash", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.face_wash_lb.grid(row=2, column=0, sticky="w")

        self.face_wash_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.face_wash_ent.grid(row=2, column=1)
        self.face_wash_ent.insert(0, 0)

        self.hair_spray_lb = Label(self.cosmetics_fm, text="Hair Spray", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.hair_spray_lb.grid(row=3, column=0, sticky="w")

        self.hair_spray_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.hair_spray_ent.grid(row=3, column=1)
        self.hair_spray_ent.insert(0, 0)

        self.hair_gel_lb = Label(self.cosmetics_fm, text="Hair Gel", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.hair_gel_lb.grid(row=4, column=0, sticky="w")

        self.hair_gel_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.hair_gel_ent.grid(row=4, column=1)
        self.hair_gel_ent.insert(0, 0)

        self.body_lotion_lb = Label(self.cosmetics_fm, text="Body Lotion", font=("Arial", 13, "bold"), bg="#df6b1e",
                                  fg="white")
        self.body_lotion_lb.grid(row=5, column=0, sticky="w")

        self.body_lotion_ent = Entry(self.cosmetics_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.body_lotion_ent.grid(row=5, column=1)
        self.body_lotion_ent.insert(0, 0)

        self.cosmetics_fm.grid(row=0, column=0, padx=2, pady=8)

        for widget in self.cosmetics_fm.winfo_children():
            widget.grid_configure(padx=10, pady=9)

        self.grocery_fm = LabelFrame(self.products_fm, text="Grocery", font=("Arial", 15, "bold"), bg="#df6b1e",
                                     fg="gray20", bd=8, relief=GROOVE)
        
        self.rice_lb = Label(self.grocery_fm, text="Rice", font=("Arial", 13, "bold"), bg="#df6b1e",
                             fg="white")
        self.rice_lb.grid(row=0, column=0, sticky="w")

        self.rice_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.rice_ent.grid(row=0, column=1)
        self.rice_ent.insert(0, 0)

        self.oil_lb = Label(self.grocery_fm, text="Oil", font=("Arial", 13, "bold"), bg="#df6b1e",
                            fg="white")
        self.oil_lb.grid(row=1, column=0, sticky="w")

        self.oil_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.oil_ent.grid(row=1, column=1)
        self.oil_ent.insert(0, 0)

        self.daal_lb = Label(self.grocery_fm, text="Daal", font=("Arial", 13, "bold"), bg="#df6b1e",
                             fg="white")
        self.daal_lb.grid(row=2, column=0, sticky="w")

        self.daal_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.daal_ent.grid(row=2, column=1)
        self.daal_ent.insert(0, 0)

        self.wheat_lb = Label(self.grocery_fm, text="Wheat", font=("Arial", 13, "bold"), bg="#df6b1e",
                              fg="white")
        self.wheat_lb.grid(row=3, column=0, sticky="w")

        self.wheat_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.wheat_ent.grid(row=3, column=1)
        self.wheat_ent.insert(0, 0)

        self.sugar_lb = Label(self.grocery_fm, text="Sugar", font=("Arial", 13, "bold"), bg="#df6b1e",
                              fg="white")
        self.sugar_lb.grid(row=4, column=0, sticky="w")

        self.sugar_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.sugar_ent.grid(row=4, column=1)
        self.sugar_ent.insert(0, 0)

        self.tea_lb = Label(self.grocery_fm, text="Tea", font=("Arial", 13, "bold"), bg="#df6b1e",
                            fg="white")
        self.tea_lb.grid(row=5, column=0, sticky="w")

        self.tea_ent = Entry(self.grocery_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.tea_ent.grid(row=5, column=1)
        self.tea_ent.insert(0, 0)
        
        self.grocery_fm.grid(row=0, column=1, padx=2, pady=8)

        for widget in self.grocery_fm.winfo_children():
            widget.grid_configure(padx=10, pady=9)

        self.cold_drinks_fm = LabelFrame(self.products_fm, text="Cold Drinks", font=("Arial", 15, "bold"), bg="#df6b1e",
                                     fg="gray20", bd=8, relief=GROOVE)
        
        self.maaza_lb = Label(self.cold_drinks_fm, text="Maaza", font=("Arial", 13, "bold"), bg="#df6b1e",
                              fg="white")
        self.maaza_lb.grid(row=0, column=0, sticky="w")

        self.maaza_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.maaza_ent.grid(row=0, column=1)
        self.maaza_ent.insert(0, 0)

        self.pepsi_lb = Label(self.cold_drinks_fm, text="Pepsi", font=("Arial", 13, "bold"), bg="#df6b1e",
                            fg="white")
        self.pepsi_lb.grid(row=1, column=0, sticky="w")

        self.pepsi_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.pepsi_ent.grid(row=1, column=1)
        self.pepsi_ent.insert(0, 0)

        self.sprite_lb = Label(self.cold_drinks_fm, text="Sprite", font=("Arial", 13, "bold"), bg="#df6b1e",
                               fg="white")
        self.sprite_lb.grid(row=2, column=0, sticky="w")

        self.sprite_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.sprite_ent.grid(row=2, column=1)
        self.sprite_ent.insert(0, 0)

        self.dew_lb = Label(self.cold_drinks_fm, text="Dew", font=("Arial", 13, "bold"), bg="#df6b1e",
                            fg="white")
        self.dew_lb.grid(row=3, column=0, sticky="w")

        self.dew_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.dew_ent.grid(row=3, column=1)
        self.dew_ent.insert(0, 0)

        self.frooti_lb = Label(self.cold_drinks_fm, text="Frooti", font=("Arial", 13, "bold"), bg="#df6b1e",
                               fg="white")
        self.frooti_lb.grid(row=4, column=0, sticky="w")

        self.frooti_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.frooti_ent.grid(row=4, column=1)
        self.frooti_ent.insert(0, 0)

        self.coke_lb = Label(self.cold_drinks_fm, text="Coca cola", font=("Arial", 13, "bold"), bg="#df6b1e",
                             fg="white")
        self.coke_lb.grid(row=5, column=0, sticky="w")

        self.coke_ent = Entry(self.cold_drinks_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.coke_ent.grid(row=5, column=1)
        self.coke_ent.insert(0, 0)
        
        self.cold_drinks_fm.grid(row=0, column=2, padx=2, pady=8)

        for widget in self.cold_drinks_fm.winfo_children():
            widget.grid_configure(padx=10, pady=9)

        self.bill_area_fm = Frame(self.products_fm, bd=8, relief=GROOVE)

        self.receipt_lb = Label(self.bill_area_fm, text="Receipt", font=("Arial", 15, "bold"), bd=7, relief=GROOVE)
        self.receipt_lb.pack(fill=X)

        self.scrollbar = Scrollbar(self.bill_area_fm, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_area = Text(self.bill_area_fm, width=54, height=18, yscrollcommand=self.scrollbar.set)
        self.text_area.pack()

        self.scrollbar.config(command=self.text_area.yview)

        self.bill_area_fm.grid(row=0, column=3, padx=10)

        self.products_fm.pack(fill=X)

        self.bill_menu_fm = LabelFrame(self.root, text="Bill Menu", font=("Arial", 15, "bold"),
                                       bg="#df6b1e", fg="gray20", bd=8, relief=GROOVE)
        
        self.cosmetic_price_lb = Label(self.bill_menu_fm, text="Cosmetic Price", font=("Arial", 13, "bold"), bg="#df6b1e",
                                       fg="white")
        self.cosmetic_price_lb.grid(row=0, column=0, sticky="w")

        self.cosmetic_price_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.cosmetic_price_ent.grid(row=0, column=1)

        self.cosmetic_tax_lb = Label(self.bill_menu_fm, text="Cosmetic Tax", font=("Arial", 13, "bold"), bg="#df6b1e",
                                     fg="white")
        self.cosmetic_tax_lb.grid(row=0, column=2, sticky="w")

        self.cosmetic_tax_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.cosmetic_tax_ent.grid(row=0, column=3)

        self.grocery_price_lb = Label(self.bill_menu_fm, text="Grocery Price", font=("Arial", 13, "bold"), bg="#df6b1e",
                                      fg="white")
        self.grocery_price_lb.grid(row=1, column=0, sticky="w")

        self.grocery_price_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.grocery_price_ent.grid(row=1, column=1)

        self.grocery_tax_lb = Label(self.bill_menu_fm, text="Grocery Tax", font=("Arial", 13, "bold"), bg="#df6b1e",
                                    fg="white")
        self.grocery_tax_lb.grid(row=1, column=2, sticky="w")

        self.grocery_tax_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.grocery_tax_ent.grid(row=1, column=3)

        self.cold_drink_price_lb = Label(self.bill_menu_fm, text="Cold Drink Price", font=("Arial", 13, "bold"), bg="#df6b1e",
                                         fg="white")
        self.cold_drink_price_lb.grid(row=2, column=0, sticky="w")

        self.cold_drink_price_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.cold_drink_price_ent.grid(row=2, column=1)

        self.cold_drink_tax_lb = Label(self.bill_menu_fm, text="Cold Drink Tax", font=("Arial", 13, "bold"), bg="#df6b1e",
                                       fg="white")
        self.cold_drink_tax_lb.grid(row=2, column=2, sticky="w")

        self.cold_drink_tax_ent = Entry(self.bill_menu_fm, font=("Arial", 15, "bold"), width=10, bd=5, relief=GROOVE)
        self.cold_drink_tax_ent.grid(row=2, column=3)

        self.button_fm = Frame(self.bill_menu_fm, bd=8, relief=GROOVE)

        self.total_btn = Button(self.button_fm, text="Total", font=("Arial", 15, "bold"), bd=5, width=8, pady=10,
                                bg="#df6b1e", fg="white", activebackground="#df6b1e", command=self.calculate_total)
        self.total_btn.grid(row=0, column=0, padx=5, pady=22)

        self.bill_btn = Button(self.button_fm, text="Bill", font=("Arial", 15, "bold"), bd=5, width=8, pady=10,
                               bg="#df6b1e", fg="white", activebackground="#df6b1e", command=self.create_receipt)
        self.bill_btn.grid(row=0, column=1, padx=5, pady=22)

        self.email_btn = Button(self.button_fm, text="Email", font=("Arial", 15, "bold"), bd=5, width=8, pady=10,
                                bg="#df6b1e", fg="white", activebackground="#df6b1e", command=self.send_email)
        self.email_btn.grid(row=0, column=2, padx=5, pady=22)

        self.print_btn = Button(self.button_fm, text="Print", font=("Arial", 15, "bold"), bd=5, width=8, pady=10,
                                bg="#df6b1e", fg="white", activebackground="#df6b1e", command=self.print_bill)
        self.print_btn.grid(row=0, column=3, padx=5, pady=22)

        self.clear_btn = Button(self.button_fm, text="Clear", font=("Arial", 15, "bold"), bd=5, width=8, pady=10,
                                bg="#df6b1e", fg="white", activebackground="#df6b1e", command=self.reset)
        self.clear_btn.grid(row=0, column=4, padx=5, pady=22)

        self.button_fm.grid(row=0, column=4, rowspan=3)

        self.bill_menu_fm.pack(fill=X)

        for widget in self.bill_menu_fm.winfo_children():
            widget.grid_configure(padx=10, pady=6)

    def calculate_total(self):
        # Calculate total cosmetic price
        soap_price = int(self.bath_soap_ent.get()) * 25
        facecream_price = int(self.face_cream_ent.get())  * 45
        facewash_price = int(self.face_wash_ent.get()) * 12
        hairspray_price = int(self.hair_spray_ent.get()) * 8
        hairgel_price = int(self.hair_gel_ent.get()) * 15
        bodylotion_price = int(self.body_lotion_ent.get()) * 18

        cosmetic_price = soap_price + facecream_price + facewash_price + hairspray_price + hairgel_price + bodylotion_price
        cosmetic_tax = cosmetic_price * (107 / 100) - cosmetic_price

        # Calculate total grocery price
        rice_price = int(self.rice_ent.get()) * 32
        oil_price = int(self.oil_ent.get()) * 8
        daal_price = int(self.daal_ent.get()) * 17
        wheat_price = int(self.wheat_ent.get()) * 12
        sugar_price = int(self.sugar_ent.get()) * 4
        tea_price = int(self.tea_ent.get()) * 16

        grocery_price = rice_price + oil_price + daal_price + wheat_price + sugar_price + tea_price
        grocery_tax = grocery_price * (107 / 100) - grocery_price

        # Calculate total drinks price
        maaza_price = int(self.maaza_ent.get()) * 2
        pepsi_price = int(self.pepsi_ent.get()) * 2
        sprite_price = int(self.sprite_ent.get()) * 2
        dew_price = int(self.dew_ent.get()) * 2
        frooti_price = int(self.frooti_ent.get()) * 3
        coke_price = int(self.coke_ent.get()) * 2

        drinks_price = maaza_price + pepsi_price + sprite_price + dew_price + frooti_price + coke_price
        drinks_tax = drinks_price * (107 / 100) - drinks_price

        self.cosmetic_price_ent.config(state="normal")
        self.cosmetic_price_ent.delete(0, END)
        self.cosmetic_price_ent.insert(0, f"$ {cosmetic_price:.2f}")
        self.cosmetic_price_ent.config(state="readonly")

        self.cosmetic_tax_ent.config(state="normal")
        self.cosmetic_tax_ent.delete(0, END)
        self.cosmetic_tax_ent.insert(0, f"$ {cosmetic_tax:.2f}")
        self.cosmetic_tax_ent.config(state="readonly")

        self.grocery_price_ent.config(state="normal")
        self.grocery_price_ent.delete(0, END)
        self.grocery_price_ent.insert(0, f"$ {grocery_price:.2f}")
        self.grocery_price_ent.config(state="readonly")

        self.grocery_tax_ent.config(state="normal")
        self.grocery_tax_ent.delete(0, END)
        self.grocery_tax_ent.insert(0, f"$ {grocery_tax:.2f}")
        self.grocery_tax_ent.config(state="readonly")

        self.cold_drink_price_ent.config(state="normal")
        self.cold_drink_price_ent.delete(0, END)
        self.cold_drink_price_ent.insert(0, f"$ {drinks_price:.2f}")
        self.cold_drink_price_ent.config(state="readonly")

        self.cold_drink_tax_ent.config(state="normal")
        self.cold_drink_tax_ent.delete(0, END)
        self.cold_drink_tax_ent.insert(0, f"$ {drinks_tax:.2f}")
        self.cold_drink_tax_ent.config(state="readonly")

        self.total_cost = cosmetic_price + cosmetic_tax + grocery_price + grocery_tax + drinks_price + drinks_tax

    def create_receipt(self):
        if self.name_ent.get() == "" or self.phone_ent.get() == "":
            messagebox.showerror("Error", "Customer Details Are Required")
            return

        elif self.cosmetic_price_ent.get() == "" and self.grocery_price_ent.get() == "" and self.cold_drink_price_ent.get() == "":
            messagebox.showerror("Error", "No Products Are Selected")
            return
        
        elif self.cosmetic_price_ent.get() == "$ 0.00" and self.grocery_price_ent.get() == "$ 0.00" and self.cold_drink_price_ent.get() == "$ 0.00":
            messagebox.showerror("Error", "No Products Are Selected")
            return
        
        self.text_area.delete("1.0", END)

        self.bill_number = random.randint(1000, 5000)
        
        self.text_area.insert(END, "** Welcome Customer **".center(54))
        self.text_area.insert(END, f"\n\nBill No.: {self.bill_number}")
        self.text_area.insert(END, f"\nCustomer Name: {self.name_ent.get()}")
        self.text_area.insert(END, f"\nPhone No.: {self.phone_ent.get()}")
        self.text_area.insert(END, "\n\n======================================================")
        self.text_area.insert(END, f"\n{"Product".ljust(22)}{"Quantity".ljust(22)}Price")
        self.text_area.insert(END, "\n======================================================")

        if self.bath_soap_ent.get() != "0":
            self.text_area.insert(END, f"\n{"Bath Soap".ljust(22)}{self.bath_soap_ent.get().ljust(22)}{int(self.bath_soap_ent.get()) * 25}")
        
        if self.face_cream_ent.get() != "0":
            self.text_area.insert(END, f"\n{"Face Cream".ljust(22)}{self.face_cream_ent.get().ljust(22)}{int(self.face_cream_ent.get())  * 45}")

        if self.face_wash_ent.get() != "0":
            self.text_area.insert(END, f"\n{"Face Wash".ljust(22)}{self.face_wash_ent.get().ljust(22)}{int(self.face_wash_ent.get()) * 12}")

        if self.hair_spray_ent.get() != "0":
            self.text_area.insert(END, f"\n{"Hair Spray".ljust(22)}{self.hair_spray_ent.get().ljust(22)}{int(self.hair_spray_ent.get()) * 8}")

        if self.hair_gel_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Hair Gel'.ljust(22)}{self.hair_gel_ent.get().ljust(22)}{int(self.hair_gel_ent.get()) * 15}")

        if self.body_lotion_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Body Lotion'.ljust(22)}{self.body_lotion_ent.get().ljust(22)}{int(self.body_lotion_ent.get()) * 18}")

        if self.rice_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Rice'.ljust(22)}{self.rice_ent.get().ljust(22)}{int(self.rice_ent.get()) * 32}")

        if self.oil_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Oil'.ljust(22)}{self.oil_ent.get().ljust(22)}{int(self.oil_ent.get()) * 8}")

        if self.daal_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Daal'.ljust(22)}{self.daal_ent.get().ljust(22)}{int(self.daal_ent.get()) * 17}")

        if self.wheat_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Wheat'.ljust(22)}{self.wheat_ent.get().ljust(22)}{int(self.wheat_ent.get()) * 12}")

        if self.sugar_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Sugar'.ljust(22)}{self.sugar_ent.get().ljust(22)}{int(self.sugar_ent.get()) * 4}")

        if self.tea_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Tea'.ljust(22)}{self.tea_ent.get().ljust(22)}{int(self.tea_ent.get()) * 16}")

        if self.maaza_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Maaza'.ljust(22)}{self.maaza_ent.get().ljust(22)}{int(self.maaza_ent.get()) * 2}")

        if self.pepsi_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Pepsi'.ljust(22)}{self.pepsi_ent.get().ljust(22)}{int(self.pepsi_ent.get()) * 2}")

        if self.sprite_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Sprite'.ljust(22)}{self.sprite_ent.get().ljust(22)}{int(self.sprite_ent.get()) * 2}")

        if self.dew_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Dew'.ljust(22)}{self.dew_ent.get().ljust(22)}{int(self.dew_ent.get()) * 2}")

        if self.frooti_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Frooti'.ljust(22)}{self.frooti_ent.get().ljust(22)}{int(self.frooti_ent.get()) * 3}")

        if self.coke_ent.get() != "0":
            self.text_area.insert(END, f"\n{'Coca cola'.ljust(22)}{self.coke_ent.get().ljust(22)}{int(self.coke_ent.get()) * 2}")

        self.text_area.insert(END, "\n------------------------------------------------------")

        if self.cosmetic_tax_ent.get() != "$ 0.00":
            self.text_area.insert(END, f"\n{'Cosmetic Tax'.ljust(30)}{self.cosmetic_tax_ent.get()}")

        if self.grocery_tax_ent.get() != "$ 0.00":
            self.text_area.insert(END, f"\n{'Grocery Tax'.ljust(30)}{self.grocery_tax_ent.get()}")

        if self.cold_drink_tax_ent.get() != "$ 0.00":
            self.text_area.insert(END, f"\n{'Cold Drink Tax'.ljust(30)}{self.cold_drink_tax_ent.get()}")

        self.text_area.insert(END, f"\n\n{'Total Bill'.ljust(30)}$ {self.total_cost:.2f}")

        self.text_area.insert(END, "\n------------------------------------------------------")

        self.save_bill()

    def save_bill(self):
        result = messagebox.askyesno("Confirm", "Do you want to save the bill?")

        if result:

            # Creates the bills directory if it does not exists
            if not os.path.exists("bills"):
                os.mkdir("bills")

            bill_content = self.text_area.get("1.0", END)

            file = open(f"bills/{self.bill_number}.txt", "w")
            file.write(bill_content)
            file.close()

            # Add bill to database
            insert_row(query="""INSERT INTO bills
                             (bill_id, name, phone, cosmetic_price, cosmetic_tax, grocery_price, grocery_tax, drink_price, drink_tax, receipt)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                             """, params=(self.bill_number, self.name_ent.get(), self.phone_ent.get(), self.cosmetic_price_ent.get(),
                                          self.cosmetic_tax_ent.get(), self.grocery_price_ent.get(), self.grocery_tax_ent.get(),
                                          self.cold_drink_price_ent.get(), self.cold_drink_tax_ent.get(), self.text_area.get("1.0", END)))

            messagebox.showinfo("Success", f"Bill Number {self.bill_number} is saved successfully")

    def search_bill(self):
        conn = sqlite3.connect("sales_orders.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bills WHERE bill_id = ?", (self.bill_ent.get(),))

        result = cursor.fetchall()
        conn.close()

        if result:
            bill_number = result[0][0]
            name = result[0][1]
            phone = result[0][2]
            cosmetic_price = result[0][3]
            cosmetic_tax = result[0][4]
            grocery_price = result[0][5]
            grocery_tax = result[0][6]
            drink_price = result[0][7]
            drink_tax = result[0][8]
            receipt = result[0][9]

            self.name_ent.delete(0, END)
            self.name_ent.insert(0, name)

            self.phone_ent.delete(0, END)
            self.phone_ent.insert(0, phone)

            self.cosmetic_price_ent.delete(0, END)
            self.cosmetic_price_ent.insert(0, cosmetic_price)

            self.cosmetic_tax_ent.delete(0, END)
            self.cosmetic_tax_ent.insert(0, cosmetic_tax)

            self.grocery_price_ent.delete(0, END)
            self.grocery_price_ent.insert(0, grocery_price)

            self.grocery_tax_ent.delete(0, END)
            self.grocery_tax_ent.insert(0, grocery_tax)

            self.cold_drink_price_ent.delete(0, END)
            self.cold_drink_price_ent.insert(0, drink_price)

            self.cold_drink_tax_ent.delete(0, END)
            self.cold_drink_tax_ent.insert(0, drink_tax)

            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", receipt)

        else:
            messagebox.showerror("Error", f"Bill Number {self.bill_ent.get()} does not exist")

    @staticmethod
    def print_file(path):
        try:
            win32api.ShellExecute(0, 'print', f"{path}/receipt.txt", None, '.', 0)

        except Exception as e:
            print(f"Error: {e}")

    def print_bill(self):
        if self.text_area.get("1.0", END).strip() != '':

            result = messagebox.askyesno("Confirm", "Do you want to print the bill?")

            if result:
                try:
                    path = askdirectory()

                    if not path:
                        return
                    
                    file_path = f"{path}/receipt.txt"

                    with open(file_path, "w") as file:
                        file.write(self.text_area.get("1.0", END))

                    threading.Thread(target=self.print_file, args=(path,), daemon=True).start()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to print: {e}")

        else:
            messagebox.showerror("Error", "No receipt to print")


    def reset(self):
        self.name_ent.delete(0, END)
        self.phone_ent.delete(0, END)
        self.bill_ent.delete(0, END)

        self.bath_soap_ent.delete(0, END)
        self.bath_soap_ent.insert(0, 0)

        self.face_cream_ent.delete(0, END)
        self.face_cream_ent.insert(0, 0)

        self.face_wash_ent.delete(0, END)
        self.face_wash_ent.insert(0, 0)

        self.hair_spray_ent.delete(0, END)
        self.hair_spray_ent.insert(0, 0)

        self.hair_gel_ent.delete(0, END)
        self.hair_gel_ent.insert(0, 0)

        self.body_lotion_ent.delete(0, END)
        self.body_lotion_ent.insert(0, 0)

        self.rice_ent.delete(0, END)
        self.rice_ent.insert(0, 0)

        self.oil_ent.delete(0, END)
        self.oil_ent.insert(0, 0)

        self.daal_ent.delete(0, END)
        self.daal_ent.insert(0, 0)

        self.wheat_ent.delete(0, END)
        self.wheat_ent.insert(0, 0)

        self.sugar_ent.delete(0, END)
        self.sugar_ent.insert(0, 0)

        self.tea_ent.delete(0, END)
        self.tea_ent.insert(0, 0)

        self.maaza_ent.delete(0, END)
        self.maaza_ent.insert(0, 0)

        self.pepsi_ent.delete(0,END)
        self.pepsi_ent.insert(0, 0)

        self.sprite_ent.delete(0, END)
        self.sprite_ent.insert(0, 0)

        self.dew_ent.delete(0, END)
        self.dew_ent.insert(0, 0)

        self.frooti_ent.delete(0, END)
        self.frooti_ent.insert(0, 0)

        self.coke_ent.delete(0, END)
        self.coke_ent.insert(0, 0)

        self.cosmetic_price_ent.delete(0, END)
        self.grocery_price_ent.delete(0, END)
        self.cold_drink_price_ent.delete(0, END)

        self.cosmetic_tax_ent.delete(0, END)
        self.grocery_tax_ent.delete(0, END)
        self.cold_drink_tax_ent.delete(0, END)

        self.text_area.delete("1.0", END)

    def send_email(self):

        def send_gmail():
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()
            ob.login(sender_ent.get(), password_ent.get())
            message = message_area.get("1.0", END)
            ob.sendmail(sender_ent.get(), receiver_ent.get(), message)
            ob.quit()
            messagebox.showinfo("Success", "Bill is successfully sent")
            

        if self.text_area.get("1.0", END).strip() != '':

            root1 = Toplevel()
            root1.title("Send Email")
            root1.config(bg="#df6b1e")
            root1.resizable(False, False)

            sender_frame = LabelFrame(root1, text="SENDER", font=("Arial", 16, "bold"), bg="#df6b1e", fg="gray20", bd=6)
            sender_frame.grid(row=0, column=0, padx=40, pady=20, sticky="snew")

            sender_lb = Label(sender_frame, text="Sender's Email", font=("Arial", 14, "bold"), bg="#df6b1e", fg="white")
            sender_lb.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            sender_ent = Entry(sender_frame, font=("Arial", 14, "bold"), bd=2, width=23, relief=RIDGE)
            sender_ent.grid(row=0, column=1, padx=10, pady=8)

            password_lb = Label(sender_frame, text="Password", font=("Arial", 14, "bold"), bg="#df6b1e", fg="white")
            password_lb.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            password_ent = Entry(sender_frame, font=("Arial", 14, "bold"), bd=2, width=23, relief=RIDGE, show="*")
            password_ent.grid(row=1, column=1, padx=10, pady=8)

            recipient_frame = LabelFrame(root1, text="RECIPIENT", font=("Arial", 16, "bold"), bg="#df6b1e", fg="gray20", bd=6)
            recipient_frame.grid(row=1, column=0, padx=40, pady=20)

            receiver_lb = Label(recipient_frame, text=  "Receiver's Email", font=("Arial", 14, "bold"), bg="#df6b1e", fg="white")
            receiver_lb.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            receiver_ent = Entry(recipient_frame, font=("Arial", 14, "bold"), bd=2, width=23, relief=RIDGE)
            receiver_ent.grid(row=0, column=1, padx=10, pady=8)

            message_lb = Label(recipient_frame, text="Message", font=("Arial", 14, "bold"), bg="#df6b1e", fg="white")
            message_lb.grid(row=1, column=0, padx=10, pady=8, sticky="w")

            message_area = Text(recipient_frame, font=("Consolas", 12, "bold"), bd=2, relief=SUNKEN, width=50, height=11)
            message_area.grid(row=2, column=0, columnspan=2)
            message_area.delete("1.0", END)
            message_area.insert(END, self.text_area.get("1.0", END).replace("=", "").replace("-", ""))

            send_btn = Button(root1, text="Send", font=("Arial", 16, "bold"), width=15, command=send_gmail)
            send_btn.grid(row=2, column=0, pady=20)

            root1.mainloop()

        else:
            messagebox.showerror("Error", "Blank receipt cannot be sent")

if __name__ == "__main__":
    init_db()
    rbs = RBS(root)
    root.mainloop()



