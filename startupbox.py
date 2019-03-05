from skimage.measure import compare_ssim  as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import urllib.request
import urllib.parse
import urllib.error
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import Label,Text
import os
import sys
from tkinter import filedialog
from tkinter import ttk


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("700x500+600+200")  # Width x Height + Position  Right + Position Left
        self.title('IRIS - Interface')

        self.frames = {}
        for F in (LoginPage, Home, Operations):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to IRIS UI", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        username = ""  # that's the given username
        password = ""  # that's the given password

        # username entry
        username_entry = Entry(self)
        username_entry.pack()

        # password entry
        password_entry = Entry(self, show='*')
        password_entry.pack()

        def trylogin():
            # check if both username and password in the entries are same of the given ones
            if username == username_entry.get() and password == password_entry.get():
                controller.show_frame("Home")
            else:
                print("Wrong")

        button = tk.Button(self, text="Log In", command=trylogin)
        button.pack()

        #button1 = tk.Button(self, text="Go to Page One",
        #                   command=lambda: controller.show_frame("PageOne"))
        #button1.pack()


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Home", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        url1 = tk.StringVar()
        url2 = tk.StringVar()

        def clicked1():
            url1 = self.url1.get()
            url2 = self.url2.get()
            self.label.configure(text=url1)
            resource = urllib.request.urlopen(url1)
            output = open("1.png", "wb")

            output.write(resource.read())
            output.close()

            resource = urllib.request.urlopen(url2)
            output = open("2.png", "wb")
            output.write(resource.read())
            output.close()

            img1 = cv2.imread("1.png")
            img2 = cv2.imread("2.png")

            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img12 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            imageA = cv2.resize(img11, (100, 100))
            imageB = cv2.resize(img12, (100, 100))

            s = ssim(imageA, imageB)

            title = "Comparing"
            fig = plt.figure(title)
            if s < 0:
                s = 0
            plt.suptitle("Percentage : %.2f " % (s * 100))

            # show first image
            ax = fig.add_subplot(1, 2, 1)
            plt.imshow(imageA, cmap=plt.cm.gray)
            plt.axis("off")

            # show the second image
            ax = fig.add_subplot(1, 2, 2)
            plt.imshow(imageB, cmap=plt.cm.gray)
            plt.axis("off")

            # show the images
            plt.show()

        def button_click():
            pass

        label = tk.Label(self, text="Image 1:")
        label.pack()
        tk.Entry(self, textvariable=url1).pack()

        label2 = tk.Label(self, text="Image 2:")
        label2.pack()
        tk.Entry(self, textvariable=url2).pack()

        submit = tk.Button(self, text='Compare Image', command=clicked1)
        submit.pack()

        def fileDialog():
            file = filedialog.askopenfile(initialdir="/", title='Choose a file', filetype=(("jpeg", "*.jpg"), ('All Files', "*.*")))
            print(file.read())

        label3 = tk.Label(self, text="      ")
        label3.pack()

        label4 = tk.Label(self, text="      ")
        label4.pack()

        button = tk.Button(self, text='Browse images', command=fileDialog)
        button.pack()


class Operations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Operations", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        def bruteforcecall():
            os.system('python runoperations.py')

        button2 = tk.Button(self, text="Bruteforce IG", command=bruteforcecall)
        button2.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
