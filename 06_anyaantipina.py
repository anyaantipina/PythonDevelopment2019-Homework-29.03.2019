#!/usr/bin/env python3
'''
Пример объектной организации кода
'''

from tkinter import *
from tkinter import colorchooser
from random import random
from math import fabs

class App(Frame):
    '''Base framed application class'''
    def __init__(self, master=None, Title="Application"):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky=N+E+S+W)
        self.create()
        self.adjust()

    def create(self):
        '''Create all the widgets'''
        self.bQuit = Button(self, text='Quit', command=self.quit)
        self.bQuit.grid()

    def adjust(self):
        '''Adjust grid sise/properties'''
        # TODO Smart detecting resizeable/still cells
        for i in range(self.size()[0]):
            self.columnconfigure(i, weight=12)
        for i in range(self.size()[1]):
            self.rowconfigure(i, weight=12)
        
class Paint(Canvas):
    '''Canvas with simple drawing'''
    def mousedown(self, event):
        '''Store mousedown coords'''
        self.x0, self.y0 = event.x, event.y
        self.cursor = None

    def mousemove(self, event):
        '''Do sometheing when drag a mouse'''
        if self.cursor:
            self.delete(self.cursor)
        self.cursor = self.create_line((self.x0, self.y0, event.x, event.y), fill=self.foreground.get())

    def mouseup(self, event):
        '''Dragging is done'''
        self.cursor = None
        #print(self.find_all())

    def __init__(self, master=None, *ap, foreground="black", **an):
        self.foreground = StringVar()
        self.foreground.set(foreground)
        Canvas.__init__(self, master, *ap, **an)
        self.bind("<Button-1>", self.mousedown)
        self.bind("<B1-Motion>", self.mousemove)
        self.bind("<ButtonRelease-1>", self.mouseup)

class MyApp(App):
    def askcolor(self):
        bg_txt = colorchooser.askcolor()[1]
        self.Canvas1.foreground.set(bg_txt)
        self.Canvas2.foreground.set(bg_txt)
        colors_bg = [int(bg_txt[1:3], 16),int(bg_txt[3:5], 16),int(bg_txt[5:7], 16)]
        fg_red = int(random()*16)
        fg_green = int(random()*16)
        fg_blue = int(random()*16)
        colors_fg = [fg_red,fg_green,fg_blue]
        for i in range(3):
            if (fabs(colors_bg[i] - colors_fg[i]) % 16) < 3:
                colors_fg[i] = (colors_fg[i] + 5) % 16
        fg_txt = '#%0x%0x%0x' % (colors_fg[0], colors_fg[1], colors_fg[2])
        self.ShowColor.configure(bg = bg_txt, fg = fg_txt)

    def copy(self, event, index):
        if (index == 1):
            for item in self.Canvas1.find_all():
                self.Canvas2.create_line((*self.Canvas1.coords(item)), fill = self.Canvas1.itemcget(item, "fill"))
        else:
            for item in self.Canvas2.find_all():
                self.Canvas1.create_line((*self.Canvas2.coords(item)), fill = self.Canvas2.itemcget(item, "fill"))

    def clean(self, event, index):
        if (index == 1):
            self.Canvas1.delete(ALL)
        else:
            self.Canvas2.delete(ALL)

    def create(self):
        self.Canvas1 = Paint(self, foreground="midnightblue")
        self.Canvas1.grid(row=0, column=0, sticky=N+E+S+W)
        self.Canvas2 = Paint(self, foreground="midnightblue")
        self.Canvas2.grid(row=1, column=0, sticky=N+E+S+W)
        frame = Frame(self)
        frame.grid(row=0, column=1, rowspan = 2, sticky = N)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        self.AskColor = Button(frame, text="Color", command=self.askcolor)
        self.AskColor.grid(row=0, column=0, sticky=N+W)
        self.ShowColor = Label(frame, textvariable=self.Canvas1.foreground, bg = "midnightblue", fg = "white")
        self.ShowColor.grid(row=1, column=0, sticky=N+W+E)
        self.Quit = Button(frame, text="Quit", command=self.quit)
        self.Quit.grid(row=6, column=0, sticky=N+W)
        self.Copy1_2 = Button(frame, text="Copy from 1 to 2")
        self.Copy1_2.bind("<Button-1>", lambda event: self.copy(event, 1))
        self.Copy1_2.grid(row=2, column=0, sticky=N+W)
        self.Copy2_1 = Button(frame, text="Copy from 2 to 1")
        self.Copy2_1.bind("<Button-1>", lambda event: self.copy(event, 2))
        self.Copy2_1.grid(row=3, column=0, sticky=N+W)
        self.Clean1 = Button(frame, text="Clean 1")
        self.Clean1.bind("<Button-1>", lambda event: self.clean(event, 1))
        self.Clean1.grid(row=4, column=0, sticky=N+W)
        self.Clean2 = Button(frame, text="Clean 2")
        self.Clean2.bind("<Button-1>", lambda event: self.clean(event, 2))
        self.Clean2.grid(row=5, column=0, sticky=N+W)

app = MyApp(Title="Canvas Example")
app.mainloop()
print ("in Canvas1: ")
for item in app.Canvas1.find_all():
    print(*app.Canvas1.coords(item), app.Canvas1.itemcget(item, "fill"))
print ("in Canvas2: ")
for item in app.Canvas2.find_all():
    print(*app.Canvas2.coords(item), app.Canvas2.itemcget(item, "fill"))

