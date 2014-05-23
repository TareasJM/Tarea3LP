#!/usr/bin/python

from Web import *

import webbrowser
from Tkinter import *
from ttk import Frame, Button, Style
from PIL import Image, ImageTk


class MainWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         

        self.parent = parent
        self.content = Canvas()
        self.canvas_objects = []
        self.vbar = 0
        self.temp = 0

        self.initUI()
        
    def initUI(self):
      
        self.parent.title("InstaCrap")
        self.style = Style()
        self.style.theme_use("default")

        self.content.pack(fill=BOTH, expand=1)

        self.web = Web();

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.content.rowconfigure(0, pad=3)
        self.content.rowconfigure(1, pad=3)
        self.content.rowconfigure(2, pad=3)
        self.content.rowconfigure(3, pad=3)
        self.content.rowconfigure(4, pad=3)
        self.content.rowconfigure(5, pad=3)

        self.vbar=Scrollbar(self.content,orient=VERTICAL)
        self.vbar.grid(row=0, column=1)
        self.vbar.config(command=self.content.yview)
        self.content.config(yscrollcommand=self.vbar.set)
        
        self.content.create_rectangle(0,100,300,200, fill="blue")

        Button(self.content, text="I'm out").grid(row=1, column=0)
        Button(self.content, text="Who?").grid(row=2, column=0) 
        Button(self.content, text="Them").grid(row=3, column=0) 
        Button(self.content, text="Me").grid(row=4, column=0) 
        Button(self.content, text="About").grid(row=5, column=0)

        button1 = Button(self, text = "Quit")
        button1_window = self.content.create_window(10, 10, window=button1)

        self.content.config(yscrollcommand=self.vbar.set)

        self.pack() 

def main():
    root = Tk()
    root.geometry("400x500+300+100")
    root.resizable(width=0, height=0)
    app = MainWindow(root)
    root.mainloop() 


if __name__ == '__main__':
    main()  