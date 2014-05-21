#!/usr/bin/python

from Tkinter import *
from ttk import Frame, Button, Style

class MainWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("InstaCrap")
        self.style = Style()
        self.style.theme_use("default")
        
        content = Canvas(self)
        content.pack(fill=BOTH, expand=1)
        for x in range(0,20,2):
            content.create_rectangle(0,0+(100*x),300,100+(100*x), fill="blue")
            content.create_rectangle(0,0+(100*(x+1)),300,100+(100*(x+1)), fill="red")
        

        vbar=Scrollbar(self,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=content.yview)
        content.config(yscrollcommand=vbar.set)

        self.pack(fill=BOTH, expand=1)
            

        outButton = Button(self, text="I'm out")
        outButton.pack(side=RIGHT)
        whoButton = Button(self, text="Who?")
        whoButton.pack(side=RIGHT)
        themButton = Button(self, text="Them")
        themButton.pack(side=RIGHT)
        meButton = Button(self, text="Me")
        meButton.pack(side=RIGHT)

        self.pack() 

def main():
    
    root = Tk()
    root.geometry("300x500+300+100")
    root.resizable(width=0, height=0)
    app = MainWindow(root)
    root.mainloop() 

if __name__ == '__main__':
    main()  