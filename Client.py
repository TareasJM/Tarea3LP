#!/usr/bin/python

from Web import *

import webbrowser
from Tkinter import *
from ttk import Frame, Button, Style
from PIL import Image, ImageTk


class MainWindow(Frame):

    """******** Funcion: __init__ && initUI **************
    Descripcion: inicializan la interfaz
    Retorno: void
    ***********************************************************************************************************************"""
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

        outButton = Button(self, text="I'm out", command=lambda: self.buttonOut())
        outButton.pack(side=RIGHT)
        whoButton = Button(self, text="Who?", command=lambda: self.buttonWho())
        whoButton.pack(side=RIGHT)
        themButton = Button(self, text="Them", command=lambda: self.buttonThem())
        themButton.pack(side=RIGHT)
        meButton = Button(self, text="Me", command=lambda: self.buttonProfile(self.web.profile_id))
        meButton.pack(side=RIGHT)
        meButton = Button(self, text="About", command=lambda: self.buttonAbout())
        meButton.pack(side=RIGHT)

        self.buttonAbout()
        self.pack() 

    """******** Funcion: clearCanvas **************
    Descripcion: vacia el contenido de la ventana
    Retorno: void
    ***********************************************************************************************************************"""
    def clearCanvas(self):
        self.content.delete("all")
        for i in range(len(self.canvas_objects)):
            try:
                self.canvas_objects[i].destroy()
            except Exception, e:
                continue
        self.content.yview_moveto(0)

    """******** Funcion: loading **************
    Descripcion: crea el texto de "loading" durante una carga de datos
    Retorno: void
    ***********************************************************************************************************************"""
    def loading(self):
        self.clearCanvas()
        self.content.create_text(200,190, text="Loading")
        self.parent.update()

    """******** Funcion: buttonToken **************
    Descripcion: Cuando es precionado token en About, se crea un cuadro para pegar un nuevo token
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonToken(self):
        self.clearCanvas()
        e = Entry(self.content)
        e.config(width=298)
        e.place(y=210)
        e.focus()
        button = Button(self.content, text="set", command=lambda: self.saveToken(e.get()))
        button.place(x=160, y=240)
        self.canvas_objects.append(e)
        self.canvas_objects.append(button)
        webbrowser.open(self.web.get_token_url)

    """******** Funcion: saveToken **************
    Descripcion: envia el nuevo token a web para que lo guarde
    Parametros:
    new_token string
    Retorno: void
    ***********************************************************************************************************************"""
    def saveToken(self, new_token):
        self.web.setToken(new_token)
        self.clearCanvas()

    """******** Funcion: buttonAbout **************
    Descripcion: genera la ventana de bienvenida e informacion de la aplicacion
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonAbout(self):
        self.clearCanvas()
        img = Image.open("icon.png")
        imgTk = ImageTk.PhotoImage(img)
        self.content.create_image(200, 100, image=imgTk)
        self.canvas_objects.append(imgTk)
        self.content.create_text(200,180, text="InstaCrap (R)")
        self.content.create_text(200,200, text="Developed by: JCastro & MSalinas")
        self.content.create_text(200,220, text="30 days evaluation copy")
        self.content.create_text(200,240, text="LP 2014-1")

        tokenButton = Button(self.content, text="Get Token", command=lambda: self.buttonToken())
        tokenButton.place(x=160, y=440)
        self.canvas_objects.append(tokenButton)
    
    """******** Funcion: buttonProfile **************
    Descripcion: pide los datos del prefil a Web y los muestra en ventana
    Parametros:
    profile_id entero
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonProfile(self, profile_id):
        self.loading()

        if self.web.token =="":
            return

        profile = self.web.profile(profile_id)
        self.clearCanvas()
        if profile == 0:
            et = '"error_type":"APINotAllowedError"'
            em = '"error_message": "you cannot view this resource"'
            self.content.create_text(200,190, text=et)
            self.content.create_text(200,210, text=em)
            return
        img = Image.open(profile['picture_file'])
        imgTk = ImageTk.PhotoImage(img)
        self.content.create_image(125, 10, anchor=NW, image=imgTk)
        self.canvas_objects.append(imgTk)

        self.content.create_text(200,190, text=profile['username'])
        self.content.create_text(200,210, text=profile['bio'])
        self.content.create_text(200,230, text=profile['website'])
        images = profile['images']
        color = ["#989898","#D6D6D6"]
        for x in range(0,len(images)):
            self.content.create_rectangle(0,350+(160*x),400,510+(160*x), fill=color[x%2])
            img = Image.open(images[x][1])
            imgTk = ImageTk.PhotoImage(img)
            self.content.create_image(80, 430+(160*x), image=imgTk)
            self.canvas_objects.append(imgTk)
            self.content.create_text(260,360+(160*x), text=images[x][2])
        if profile['following'] == 0:
            button = Button(self.content, text="Follow", command=lambda: self.follow(1,profile["profile_id"]))
            button_window = self.content.create_window(200, 250, window=button)
            self.canvas_objects.append(button)
            self.canvas_objects.append(button_window)
        elif profile["following"] == 1:
            button = Button(self.content, text="Unfollow", command=lambda: self.follow(0,profile["profile_id"]))
            button_window = self.content.create_window(200, 250, window=button)
            self.canvas_objects.append(button)
            self.canvas_objects.append(button_window)
    
    """******** Funcion: buttonThem **************
    Descripcion: pide los datos de feed a Web y los muestra en la ventana
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonThem(self):
        if self.web.token =="":
            return
        self.loading()
        feeds = self.web.feed()
        self.clearCanvas()

        color = ["#989898","#D6D6D6"]
        for x in range(0,len(feeds)):
            self.content.create_rectangle(0,(160*x),400,160+(160*x), fill=color[x%2])
            img = Image.open(feeds[x][2])
            imgTk = ImageTk.PhotoImage(img)
            self.content.create_image(80,80+(160*x), image=imgTk)
            self.canvas_objects.append(imgTk)
            self.content.create_text(260,10+(160*x), text=feeds[x][0])
            self.content.create_text(260,30+(160*x), text=feeds[x][3])
    
    """******** Funcion: buttonWho **************
    Descripcion: crea un cuadro para ingresar el string a buscar
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonWho(self):
        if self.web.token =="":
            return
        self.clearCanvas()
        e = Entry(self.content)
        e.config(width=298)
        e.place(y=210)
        e.focus()
        button = Button(self.content, text="search", command=lambda: self.search(e.get()))
        button.place(x=160, y=240)
        self.canvas_objects.append(e)
        self.canvas_objects.append(button)

    """******** Funcion: search **************
    Descripcion: pide a Web que busque el string ingresado
    Parametros:
    string string 
    Retorno: void
    ***********************************************************************************************************************"""
    def search(self, string):
        self.loading()
        results = self.web.search(string)
        self.clearCanvas()
        color = ["#989898","#D6D6D6"]
        if len(results) == 0:
            self.content.create_text(200,10, text="No results")
        else:
            func = [0]*len(results)
            for x in range(0,len(results)):
                profile = results[x]

                self.content.create_rectangle(0,(160*x),400,160+(160*x), fill=color[x%2])

                img = Image.open(profile[3])
                imgTk = ImageTk.PhotoImage(img)
                self.content.create_image(5, 5+(160*x), anchor=NW, image=imgTk)
                self.canvas_objects.append(imgTk)

                self.content.create_text(275,10+(160*x), text=profile[0].replace('\\',''))
                self.content.create_text(275,30+(160*x), text=profile[1].replace('\\',''))
                self.content.create_text(275,50+(160*x), text=profile[2].replace('\\',''))

                view = Button(self.content, text="View Profile", command=lambda pid=profile[5]: self.buttonProfile(pid))
                view_window = self.content.create_window(275, 100+(160*x), window=view)
                self.canvas_objects.append(view)
                self.canvas_objects.append(view_window)
                self.content.pack()

    """******** Funcion: follow **************
    Descripcion: envia los datos de un perfil a web para follow/Unfollow
    Parametros:
    follow entero
    profile_id entero
    Retorno: void
    ***********************************************************************************************************************"""
    def follow(self, follow, profile_id):
        self.loading()
        self.web.follow(follow, profile_id)
        self.buttonProfile(profile_id)

    """******** Funcion: buttonOut **************
    Descripcion: finaliza la aplicacion
    Retorno: void
    ***********************************************************************************************************************"""
    def buttonOut(self):
        raise SystemExit

def main():
    root = Tk()
    root.geometry("400x500+300+100")
    root.resizable(width=0, height=0)
    app = MainWindow(root)
    root.mainloop() 


if __name__ == '__main__':
    main()  