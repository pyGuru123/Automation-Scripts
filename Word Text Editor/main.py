import tkinter as tk
from docx import Document

class Application(tk.Tk):
	def __init__(self):
		super().__init__()

		# Variables
		self.name = tk.StringVar()

		self.draw_frames()
		self.draw_top_frame()
		self.draw_bottom_frame()

	def draw_frames(self):
		self.top = tk.Frame(self, width="640", height="380", bg='gray8')
		self.top.grid(row=0, column=0)
		self.top.grid_propagate(False)

		self.bottom = tk.Frame(self, width="640", height="100", bg="gray75")
		self.bottom.grid(row=1, column=0)
		self.bottom.grid_propagate(False)

	def draw_top_frame(self):
		lbl1 = tk.Label(self.top, text="Enter Name", fg='white', bg="gray8", font=('Calibri', 12))
		lbl1.grid(row=0, column=0)

		self.input1 = tk.Entry(self.top, textvariable=self.name)
		self.input1.grid(row=0, column=1)

	def draw_bottom_frame(self):
		self.button1 = tk.Button(self.bottom, text="Save Word", command=self.updateWord)
		self.button1.grid(row=0, column=0)

	def updateWord(self):
		print(self.name.get())
		print("Something is being done")

if __name__ == '__main__':
	app = Application()
	app.title('Word Editor')
	app.geometry('640x480+300+100')
	app.mainloop()