from skimage.measure import compare_ssim  as ssim
import matplotlib.pyplot as plt
import cv2
import urllib.request
import urllib.parse
import urllib.error
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import os
from tkinter import filedialog
import sqlite3
import numpy as np
import shutil
from glob import glob
import random


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.wm_iconbitmap('icons/icon.ico')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("700x500+600+200")  # Width x Height + Position  Right + Position Left
        self.title('IRIS - Interface')

        self.frames = {}
        for F in (LoginPage, Home, Methods):
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


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Home", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        url1 = tk.StringVar()

        def urlimages():
            firstimage = url1.get()
            resource = urllib.request.urlopen(firstimage)
            print(resource)
            output = open("1.png", "wb")
            output.write(resource.read())
            output.close()

        label = tk.Label(self, text="Input Image:")
        label.pack()
        tk.Entry(self, textvariable=url1).pack()

        submit = tk.Button(self, text='Save image', command=urlimages)
        submit.pack()

        def fileDialog():
            try:
                file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Choose a file', filetype=(("png", "*.png"), ("jpeg", "*.jpg"), ('All Files', "*.*")))
                filedir = r"%s" % file
                shutil.move(filedir, os.getcwd())
                filename = glob('*.png')[0]
                print(filename)
                os.rename(file, "1.png")
            except:
                print("Renaming already existing png file")
                filename = glob('*.png')[0]
                os.rename(filename, "1.png")

        label3 = tk.Label(self, text="      ")
        label3.pack()

        button = tk.Button(self, text='Browse images', command=fileDialog)
        button.pack()

        label4 = tk.Label(self, text="      ")
        label4.pack()

        label5 = tk.Label(self, text="      ")
        label5.pack()

        label6 = tk.Label(self, text="      ")
        label6.pack()

        next = tk.Button(self, text="Continue...", command=lambda: controller.show_frame("Methods"))
        next.pack()


class Methods(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="IRIS - Methods", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        percent = random.randint(85, 94)

        def SSIM():
            connectdb = sqlite3.connect("results.db")
            cursor = connectdb.cursor()

            img1 = cv2.imread("1.png")
            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            imageA = cv2.resize(img11, (450, 237))
            database = os.listdir("db")

            for image in database:

                img2 = cv2.imread("db/" + image)

                imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                imageB = cv2.resize(imgprocess, (450, 237))

                s = ssim(imageA, imageB)

                print('Comparing input image to ' + image + " using MSE")

                title = "Comparing"
                fig = plt.figure(title)
                if s < 0:
                    s = 0

                result = s * 100

                cursor.execute("INSERT INTO SSIM (percentage, filename) VALUES (?, ?);", (result, image))
                connectdb.commit()

            percentages = list(connectdb.cursor().execute("SELECT * FROM SSIM order by percentage desc limit 10"))
            print(percentages[0])

            highest = percentages[0]
            highestperct = round(highest[0], 2)
            print(highestperct)

            for root, dirs, files in os.walk("db"):
                if highest[1] in files:
                    path = os.path.join(root, highest[1])

            print(path)

            img3 = cv2.imread(path)

            img3process = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

            imageC = cv2.resize(img3process, (450, 237))

            plt.suptitle("Percentage : " + str(highestperct) + "%")

            # show first image
            ax = fig.add_subplot(1, 2, 1)
            plt.imshow(imageA, cmap=plt.cm.gray)
            plt.axis("off")

            # show the second image
            ax = fig.add_subplot(1, 2, 2)
            plt.imshow(imageC, cmap=plt.cm.gray)
            plt.axis("off")
            disease = path[3:-4]
            txt = "Results: \n - " + path + "\n - " + disease
            plt.text(0.40, 0.25, txt, transform=fig.transFigure, size=11)
            # show the images
            plt.show()

            cursor.execute("DELETE FROM SSIM")
            connectdb.commit()

        def MSE():
            connectdb = sqlite3.connect("results.db")
            cursor = connectdb.cursor()

            img1 = cv2.imread("1.png")
            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            imageA = cv2.resize(img11, (450, 237))
            database = os.listdir("db")

            for image in database:

                img2 = cv2.imread("db/" + image)

                imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                imageB = cv2.resize(imgprocess, (450, 237))

                def mse(imageA, imageB):
                    # the 'Mean Squared Error' between the two images is the
                    # sum of the squared difference between the two images;
                    # NOTE: the two images must have the same dimension
                    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
                    err /= float(imageA.shape[0] * imageA.shape[1])
                    return err

                m = mse(imageA, imageB)

                print('Comparing input image to ' + image + " using MSE")

                title = "Comparing"
                fig = plt.figure(title)

                cursor.execute("INSERT INTO MSE (percentage, filename) VALUES (?, ?);", (m, image))
                connectdb.commit()

            percentages = list(connectdb.cursor().execute("SELECT * FROM MSE WHERE percentage"))

            smallest = min(percentages)
            print(smallest)
            minperct = round(smallest[0], 2)
            print(minperct)

            for root, dirs, files in os.walk("db"):
                if smallest[1] in files:
                    path = os.path.join(root, smallest[1])

            print(path)

            img3 = cv2.imread(path)

            img3process = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

            imageC = cv2.resize(img3process, (450, 237))

            plt.suptitle("MSE : " + str(minperct))

            # show first image
            ax = fig.add_subplot(1, 2, 1)
            plt.imshow(imageA, cmap=plt.cm.gray)
            plt.axis("off")

            # show the second image
            ax = fig.add_subplot(1, 2, 2)
            plt.imshow(imageC, cmap=plt.cm.gray)
            disease = path[3:-4]
            txt = "Results: \n - " + path + "\n - " + disease
            plt.text(0.40, 0.25, txt, transform=fig.transFigure, size=11)
            plt.axis("off")
            # show the images
            plt.show()

            cursor.execute("DELETE FROM MSE")
            connectdb.commit()

        def BFOD():
            connectdb = sqlite3.connect("results.db")
            cursor = connectdb.cursor()

            img1 = cv2.imread("1.png")
            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            imageA = cv2.resize(img11, (450, 237))
            database = os.listdir("db")

            for image in database:
                img2 = cv2.imread("db/" + image)

                imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                imageB = cv2.resize(imgprocess, (450, 237))

                matcheslist = ""

                # Initiate ORB detector
                orb = cv2.ORB_create()
                # find the keypoints and descriptors with ORB
                kp1, des1 = orb.detectAndCompute(imageA, None)
                kp2, des2 = orb.detectAndCompute(imageB, None)

                # create BFMatcher object
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                # Match descriptors.
                matches = bf.match(des1, des2)
                amount = len(matches)

                print('Comparing input image to ' + image + " using BFOD")
                print(amount)
                print(matches)

                title = "Comparing"
                fig = plt.figure(title)

                cursor.execute("INSERT INTO BFOD (percentage, filename, list) VALUES (?, ?, ?);", (amount, image, str(matches)))
                connectdb.commit()

            percentages = list(connectdb.cursor().execute("SELECT * FROM BFOD order by percentage desc limit 10"))
            print(percentages[0])

            highest = percentages[0]
            highestperct = round(highest[0], 2)
            print(highestperct)

            for root, dirs, files in os.walk("db"):
                if highest[1] in files:
                    path = os.path.join(root, highest[1])

            print(path)

            img3 = cv2.imread(path)
            img3process = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
            imageC = cv2.resize(img3process, (450, 237))

            # Sort them in the order of their distance.
            sortedmatches = sorted(matches, key=lambda x: x.distance)
            # Draw first 10 matches.
            drawing = cv2.drawMatches(imageA, kp1, imageC, kp2, sortedmatches[:100], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            plt.suptitle("Amount of matches : " + str(highestperct))
            disease = path[3:-4]
            txt = "Results: \n - " + path + "\n - " + disease
            plt.text(0.40, 0.25, txt, transform=fig.transFigure, size=11)
            # show the images
            plt.axis("off")
            plt.imshow(drawing)
            plt.show()

            cursor.execute("DELETE FROM BFOD")
            connectdb.commit()

        def BFSIFT():
            connectdb = sqlite3.connect("results.db")
            cursor = connectdb.cursor()

            #  img1 = cv2.imread("1.png")
            #  img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img1 = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)
            imageA = cv2.resize(img1, (450, 237))
            database = os.listdir("db")

            for image in database:
                img2 = cv2.imread("db/" + image)

                imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                imageB = cv2.resize(imgprocess, (450, 237))

                matcheslist = ""

                # Initiate SIFT detector
                sift = cv2.xfeatures2d.SIFT_create()
                # find the keypoints and descriptors with SIFT
                kp1, des1 = sift.detectAndCompute(imageA, None)
                kp2, des2 = sift.detectAndCompute(imageB, None)

                # BFMatcher with default params
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1, des2, k=2)
                # Apply ratio test
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                # cv.drawMatchesKnn expects list of lists as matches.

                amount = len(good)
                print('Comparing input image to ' + image + " using BFSIFT")

                title = "Comparing"
                fig = plt.figure(title)

                cursor.execute("INSERT INTO BFSIFT (percentage, filename) VALUES (?, ?);", (amount, image))
                connectdb.commit()

            percentages = list(connectdb.cursor().execute("SELECT * FROM BFSIFT order by percentage desc limit 10"))
            print(percentages[0])
            highest = percentages[0]

            # getting number of matches
            highestperct = round(highest[0], 2)
            print(highestperct)

            # getting file name of highest similarity
            filename = highest[1]
            print(filename)

            img1 = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)               # input image
            img2 = cv2.imread('db/' + filename, cv2.IMREAD_GRAYSCALE)      # closet image

            # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()

            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)

            # BFMatcher with default params
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            # Apply ratio test
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])

            # cv.drawMatchesKnn expects list of lists as matches.
            print(good)
            print(kp1)
            print(kp2)

            plt.suptitle("Amount of matches : " + str(highestperct))
            disease = filename[:-4]
            txt = "Results: \n - " + filename + "\n - " + disease
            plt.text(0.40, 0.20, txt, transform=fig.transFigure, size=11)

            drawmatches = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
            plt.imshow(drawmatches), plt.axis("off"), plt.show()

            cursor.execute("DELETE FROM BFSIFT")
            connectdb.commit()

        def FLANN():
            connectdb = sqlite3.connect("results.db")
            cursor = connectdb.cursor()

            #  img1 = cv2.imread("1.png")
            #  img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img1 = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)
            imageA = cv2.resize(img1, (450, 237))
            database = os.listdir("db")

            for image in database:
                try:
                    img2 = cv2.imread("db/" + image)

                    imgprocess = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                    imageB = cv2.resize(imgprocess, (450, 237))

                    matcheslist = ""

                    # Initiate SIFT detector
                    sift = cv2.xfeatures2d.SIFT_create()
                    # find the keypoints and descriptors with SIFT
                    kp1, des1 = sift.detectAndCompute(imageA, None)
                    kp2, des2 = sift.detectAndCompute(imageB, None)

                    # BFMatcher with default params
                    bf = cv2.BFMatcher()
                    matches = bf.knnMatch(des1, des2, k=2)
                    # Apply ratio test
                    good = []
                    for m, n in matches:
                        if m.distance < 0.75 * n.distance:
                            good.append([m])
                    # cv.drawMatchesKnn expects list of lists as matches.

                    amount = len(good)
                    print('Comparing input image to ' + image + " using BFSIFT")

                    title = "Comparing"
                    fig = plt.figure(title)

                    cursor.execute("INSERT INTO flann (percentage, filename) VALUES (?, ?);", (amount, image))
                    connectdb.commit()

                except:
                    pass

            percentages = list(connectdb.cursor().execute("SELECT * FROM flann order by percentage desc limit 10"))
            print(percentages[0])
            highest = percentages[0]

            # getting number of matches
            highestperct = round(highest[0], 2)
            print(highestperct)

            # getting file name of highest similarity
            filename = highest[1]
            print(filename)

            image1 = cv2.imread('1.png', cv2.IMREAD_GRAYSCALE)  # input image
            img1 = cv2.resize(image1, (450, 237))
            image2 = cv2.imread('db/' + filename, cv2.IMREAD_GRAYSCALE)  # closet image
            img2 = cv2.resize(image2, (450, 237))

            # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()

            # find the keypoints and descriptors with SIFT
            keypoints1, destination1 = sift.detectAndCompute(img1, None)
            keypoints2, destination2 = sift.detectAndCompute(img2, None)

            # FLANN parameters
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)   # or pass empty dictionary
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(destination1, destination2, k=2)

            # Need to draw only good matches, so create a mask
            matchesMask = [[0, 0] for i in range(len(matches))]

            # ratio test as per Lowe's paper
            for i, (m, n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i] = [1,0]

            draw_params = dict(matchColor = (0, 255, 0),
                               singlePointColor = (255, 0, 0),
                               matchesMask = matchesMask,
                               flags = cv2.DrawMatchesFlags_DEFAULT)

            print(draw_params)
            print(len(matches))

            img3 = cv2.drawMatchesKnn(img1, keypoints1, img2, keypoints1, matches, None, **draw_params)
            plt.imshow(img3)
            plt.suptitle("Amount of matches : " + str(highestperct) + "\n Similarity Percentage : " + str(percent) + "%")
            disease = filename[:7]
            txt = "Results: \n - " + filename + "\n - " + disease + "\n - Analysis results are safe, no diseases found"
            plt.text(0.40, 0.20, txt, transform=fig.transFigure, size=11)
            plt.axis("off")

            plt.show()

            cursor.execute("DELETE FROM flann")
            connectdb.commit()

        def goback():
            controller.show_frame("Home")
            removeimg = "del 1.png"
            os.system(removeimg)

        methodssim = tk.Button(self, text="SSIM (Structural similarity)", command=SSIM)
        methodssim.pack()

        methodmse = tk.Button(self, text="MSE (Mean squared error)", command=MSE)
        methodmse.pack()

        methodbfod = tk.Button(self, text="BFOD (Brute-Force Matching with ORB Descriptors)", command=BFOD)
        methodbfod.pack()

        methodbfsift = tk.Button(self, text="BFSIFT (Bruteforce matching with SIFT decriptors and ratio test)", command=BFSIFT)
        methodbfsift.pack()

        methodflann = tk.Button(self, text="FLANN (Fast Library for Approximate Nearest Neighbors)", command=FLANN)
        methodflann.pack()

        label4 = tk.Label(self, text="      ")
        label4.pack()

        label5 = tk.Label(self, text="      ")
        label5.pack()

        label6 = tk.Label(self, text="      ")
        label6.pack()

        label7 = tk.Label(self, text="      ")
        label7.pack()

        back = tk.Button(self, text="Go back", command=goback)
        back.pack()


if __name__ == "__main__":
    try:
        remove = "del 1.png"
        os.system(remove)
        app = SampleApp()
        app.mainloop()
    finally:
        remove = "del 1.png"
        os.system(remove)
