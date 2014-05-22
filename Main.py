#!/usr/bin/python

from Web import *

import webbrowser
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

        content = Canvas()
        content.pack(fill=BOTH, expand=1)

        self.web = Web();
        
        vbar=Scrollbar(self,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=content.yview)
        content.config(yscrollcommand=vbar.set)
        content.config(scrollregion=(0, 0, 0, 0))

        content.create_rectangle(0,0,300,100, fill="green")

        tokenButton = Button(content, text="Get Token", command=lambda: self.buttonToken(tokenButton, content))
        tokenButton.place(x=110, y=240)

        outButton = Button(self, text="I'm out", command=self.buttonOut)
        outButton.pack(side=RIGHT)
        whoButton = Button(self, text="Who?", command=self.buttonWho(content))
        whoButton.pack(side=RIGHT)
        themButton = Button(self, text="Them", command=lambda: self.buttonThem(content))
        themButton.pack(side=RIGHT)
        meButton = Button(self, text="Me", command=lambda: self.buttonMe(content))
        meButton.pack(side=RIGHT)

        self.pack() 

    def buttonToken(self, button, content):
        button.destroy()
        content.delete("all")
        e = Entry(content)
        e.config(width=298)
        e.place(y=210)
        e.focus()
        button = Button(content, text="set", command=lambda: self.saveToken(e.get(), content, button, e))
        button.place(x=110, y=240)
        webbrowser.open(self.web.get_token_url)

    def saveToken(self, new_token, content, button, entry):
        self.web.setToken(new_token)
        content.delete("all")
        entry.destroy()
        button.destroy()

    def buttonThem(self, content):
        if self.web.token =="":
            return
        content.delete("all")
        for x in range(0,20,2):
            content.create_rectangle(0,0+(100*x),300,100+(100*x), fill="blue")
            content.create_rectangle(0,0+(100*(x+1)),300,100+(100*(x+1)), fill="red")

        content.config(scrollregion=(0, 1520, 0, 480))
    
    def buttonMe(self, content):
        if self.web.token =="":
            return
        content.delete("all")
        profile = self.web.myProfile()

        content.create_text(150,10, text=profile['username'])
        content.create_text(150,30, text=profile['bio'])
        content.create_text(150,50, text=profile['website'])
        content.create_text(150,70, text=profile['profile_picture'])
    
    def buttonWho(self, content):
        if self.web.token =="":
            return
        content.delete("all")

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