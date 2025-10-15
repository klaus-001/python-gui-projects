import requests
import json
import os

from tkinter import *
from dotenv import load_dotenv

def load_data():
    url = f'https://openexchangerates.org/api/latest.json?app_id={os.getenv('app_id')}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.HTTPError:
        match response.status_code:
            case 400:
                return {'error': 'Invalid base'}
            case 401:
                return {'error': 'Invalid App ID'}
            case 403:
                return {'error': 'Access restricted'}
            case 404:
                return {'error': 'Not found'}
            case 429:
                return {'error': 'Not allowed'}
                    
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection error'}
        
    except requests.exceptions.Timeout:
       return {'error': 'Request timed out'}
        
    except requests.exceptions.TooManyRedirects:
        return {'error': 'Check the URL'}

    except requests.exceptions.RequestException:
        return {'error': 'Request error'}

def convert(base, to, amount):
    data = load_data()
    
    if 'error' in data:
        return {'error': data['error']}
    
    rates = data['rates']
    from_rates = rates.get(base)
    to_rates = rates.get(to)

    # Checks if rates are valid
    if from_rates is None and base != 'USD':
        return {'error': 'Invalid base currency'}
    if to_rates is None and to != 'USD':
        return {'error': 'Invalid target currency'}

    # Return the rates
    if base == 'USD':
        return amount * to_rates
    elif to == 'USD':
        return amount / from_rates
    else:
        return amount * (to_rates / from_rates)

def submit():
    global conversion_text, amount_text
    
    # Gets the user input
    base = convert_from.get().upper()
    to = convert_to.get().upper()
    
    try:
        amount = int(amount_entry.get())
        
        result = convert(base, to, amount)
    
        if isinstance(result, dict):
            conversion_text = result['error']
            amount_text = ''
        else:
            conversion_text = f'{base} to {to}'
            amount_text = f'{result:.2f}'
        
        conversion_label.set(conversion_text)
        amount_label.set(amount_text)

    except ValueError:
        conversion_text = 'Please check inputs'
        conversion_label.set(conversion_text)
        
        amount_text = 'Enter numeric amount'
        amount_label.set(amount_text)
        
def reset():
    global conversion_text, amount_text
    
    # Reset top label
    conversion_text = ''
    conversion_label.set(conversion_text)
    
    # Reset bottom label
    amount_text = ''
    amount_label.set(amount_text)
    
    # Reset entry box
    convert_from.config(fg='#AAAAAA', font=('Helvetica', 12, 'italic'))
    convert_from.delete(0, END)
    convert_from.insert(0, 'Enter currency to convert from:')
    
    convert_to.config(fg='#AAAAAA', font=('Helvetica', 12, 'italic'))
    convert_to.delete(0, END)
    convert_to.insert(0, 'Enter currency to convert to:')
    
    amount_entry.config(fg='#AAAAAA', font=('Helvetica', 12, 'italic'))
    amount_entry.delete(0, END)
    amount_entry.insert(0, 'Amount:')
    
    window.focus() # remove focus from entry fields
    
def clear_entry(event):
    event.widget.delete(0, END)
    event.widget.config(fg='black', font=('Helvetica', 12, 'italic'))

load_dotenv()

window = Tk()
window.title('Currency Exchange')
window.resizable(False, False)

conversion_text = ''
conversion_label = StringVar()

amount_text = ''
amount_label = StringVar()

top_label = Label(window,
                  textvariable=conversion_label,
                  fg='white',
                  bg='black',
                  font=('Helvetica', 30),
                  width=18,
                  height=3)
top_label.pack()

bottom_label = Label(window,
                     textvariable=amount_label,
                     fg='white',
                     bg='black',
                     font=('Helvetica', 30),
                     width=18,
                     height=3)
bottom_label.pack()

convert_from = Entry(window, fg='#AAAAAA', font=('Helvetica', 12, 'italic'), width=35)
convert_from.insert(0, 'Enter currency to convert from:')
convert_from.bind('<FocusIn>', clear_entry)
convert_from.pack(anchor='w', padx=10, pady=10)

convert_to = Entry(window, fg='#AAAAAA', font=('Helvetica', 12, 'italic'), width=35)
convert_to.insert(0, 'Enter currency to convert to:')
convert_to.bind('<FocusIn>', clear_entry)
convert_to.pack(anchor='w', padx=10)

amount_entry = Entry(window, fg='#AAAAAA', font=('Helvetica', 12, 'italic'), width=35)
amount_entry.insert(0, 'Amount:')
amount_entry.bind('<FocusIn>', clear_entry)
amount_entry.pack(anchor='w', padx=10, pady=10)

frame = Frame(window)
frame.pack(pady=13)

submit = Button(frame, text='Submit', font=('Helvetica', 12, 'bold'), padx=5, command=submit)
submit.pack(side='left', padx=7)

reset = Button(frame, text='Reset', font=('Helvetica', 12, 'bold'), padx=5, command=reset)
reset.pack(side='left', padx=7)

window.mainloop()
