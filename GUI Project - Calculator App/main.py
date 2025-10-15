
from tkinter import *

class Calculator:
	def __init__(self, window):
		self.window = window

		self.window.geometry('500x600')
		self.window.resizable(False, False)

		self.window.title('Calculator App')

		self.equation_text = ''

		self.create_widgets()

	def create_widgets(self):
		self.equation_label = StringVar()

		self.label = Label(self.window, textvariable=self.equation_label, font=('consolas', 20), bg='white', width=28, height=2)
		self.label.pack()

		self.frame = Frame(self.window)
		self.frame.pack()

		self.button1 = Button(self.frame, text=1, height=4, width=9, font=35,
						command=lambda: self.button_press(1))
		self.button1.grid(row=0, column=0)

		self.button2 = Button(self.frame, text=2, height=4, width=9, font=35,
						command=lambda: self.button_press(2))
		self.button2.grid(row=0, column=1)

		self.button3 = Button(self.frame, text=3, height=4, width=9, font=35,
						command=lambda: self.button_press(3))
		self.button3.grid(row=0, column=2)

		self.button4 = Button(self.frame, text=4, height=4, width=9, font=35,
						command=lambda: self.button_press(4))
		self.button4.grid(row=1, column=0)

		self.button5 = Button(self.frame, text=5, height=4, width=9, font=35,
						command=lambda: self.button_press(5))
		self.button5.grid(row=1, column=1)

		self.button6 = Button(self.frame, text=6, height=4, width=9, font=35,
						command=lambda: self.button_press(6))
		self.button6.grid(row=1, column=2)

		self.button7 = Button(self.frame, text=7, height=4, width=9, font=35,
						command=lambda: self.button_press(7))
		self.button7.grid(row=2, column=0)

		self.button8 = Button(self.frame, text=8, height=4, width=9, font=35,
						command=lambda: self.button_press(8))
		self.button8.grid(row=2, column=1)

		self.button9 = Button(self.frame, text=9, height=4, width=9, font=35,
						command=lambda: self.button_press(9))
		self.button9.grid(row=2, column=2)

		self.button0 = Button(self.frame, text=0, height=4, width=9, font=35,
						command=lambda: self.button_press(0))
		self.button0.grid(row=3, column=0)

		self.plus = Button(self.frame, text='+', height=4, width=9, font=35,
						command=lambda: self.button_press('+'))
		self.plus.grid(row=0, column=3)

		self.minus = Button(self.frame, text='-', height=4, width=9, font=35,
						command=lambda: self.button_press('-'))
		self.minus.grid(row=1, column=3)

		self.multiply = Button(self.frame, text='*', height=4, width=9, font=35,
						command=lambda: self.button_press('*'))
		self.multiply.grid(row=2, column=3)

		self.divide = Button(self.frame, text='/', height=4, width=9, font=35,
						command=lambda: self.button_press('/'))
		self.divide.grid(row=3, column=3)

		self.equal = Button(self.frame, text='=', height=4, width=9, font=35,
						command=self.equals)
		self.equal.grid(row=3, column=2)

		self.decimal = Button(self.frame, text='.', height=4, width=9, font=35,
						command=lambda: self.button_press('.'))
		self.decimal.grid(row=3, column=1)

		self.clear = Button(self.window, text='clear', height=4, width=12, font=35,
					command=self.clear)
		self.clear.pack()

	def button_press(self, num):
		self.equation_text = self.equation_text + str(num)
		self.equation_label.set(self.equation_text)
	
	def equals(self):
		try:
			total = str(eval(self.equation_text)) # eval will parse the expression

			self.equation_label.set(total)
			self.equation_text = total
		
		except SyntaxError:	
			self.equation_label.set('Syntax error')
			
		except ZeroDivisionError:
			self.equation_label.set('Arithmetic error')
	
	def clear(self):
		self.equation_label.set('')
		self.equation_text = ''


if __name__ == '__main__':
	window = Tk()
	calculator = Calculator(window)
	window.mainloop()
