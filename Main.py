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
        
        self.vbar=Scrollbar(self,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.content.yview)
        self.content.config(yscrollcommand=self.vbar.set)

        tokenButton = Button(self.content, text="Get Token", command=lambda: self.buttonToken(tokenButton))
        tokenButton.place(x=110, y=240)
        self.canvas_objects.append(tokenButton)

        outButton = Button(self, text="I'm out", command=lambda: self.buttonOut())
        outButton.pack(side=RIGHT)
        whoButton = Button(self, text="Who?", command=lambda: self.buttonWho())
        whoButton.pack(side=RIGHT)
        themButton = Button(self, text="Them", command=lambda: self.buttonThem())
        themButton.pack(side=RIGHT)
        meButton = Button(self, text="Me", command=lambda: self.buttonMe())
        meButton.pack(side=RIGHT)

        self.pack() 

    def clearCanvas(self):
        self.content.delete("all")
        for i in range(len(self.canvas_objects)):
            self.canvas_objects[i].destroy()
        self.content.yview_moveto(0)

    def buttonToken(self, button):
        self.clearCanvas()
        e = Entry(self.content)
        e.config(width=298)
        e.place(y=210)
        e.focus()
        button = Button(self.content, text="set", command=lambda: self.saveToken(e.get()))
        button.place(x=110, y=240)
        webbrowser.open(self.web.get_token_url)

    def saveToken(self, new_token):
        self.web.setToken(new_token)
        self.clearCanvas()

    def buttonThem(self):
        if self.web.token =="":
            return
        self.clearCanvas()
        for x in range(0,20,2):
            self.content.create_rectangle(0,0+(100*x),300,100+(100*x), fill="blue")
            self.content.create_rectangle(0,0+(100*(x+1)),300,100+(100*(x+1)), fill="red")
    
    def buttonMe(self):
        if self.web.token =="":
            return
        self.clearCanvas()
        profile = self.web.myProfile()

        img = Image.open(profile['picture_file'])
        imgTk = ImageTk.PhotoImage(img)
        self.content.create_image(75, 10, anchor=NW, image=imgTk)
        self.canvas_objects.append(imgTk)

        self.content.create_text(150,190, text=profile['username'])
        self.content.create_text(150,210, text=profile['bio'])
        self.content.create_text(150,230, text=profile['website'])

        for x in range(0,20,2):
            self.content.create_rectangle(0,350+(100*x),300,450+(100*x), fill="blue")
            self.content.create_rectangle(0,350+(100*(x+1)),300,450+(100*(x+1)), fill="green")
    
    def buttonWho(self):
        if self.web.token =="":
            return
        self.clearCanvas()

    def buttonOut(self):
        raise SystemExit

def main():
    root = Tk()
    root.geometry("300x500+300+100")
    root.resizable(width=0, height=0)
    app = MainWindow(root)
    root.mainloop() 


if __name__ == '__main__':
    main()  