from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from AsciiConvertor import ImageToConvert

class GUI:
    mon = Image
    col = Image
    def __init__(self, file_name:str, scale:float):
        root = Tk()

        im = ImageToConvert(file_name)      #otevre obrazek
        im.scale(scale)                       #skaluje obrazek

        im.imageToText("reverse")           #prevede obrazek na text ze znaku ze znakove sady reverse

        monochromeim = im.textToImage()     #prevede tex na obrazek
        colourim = im.imageToColorImage("long") #prevede obrazek na obrazek ze znaku ze znakove sady long

        ### skaluje obrazky a upravi pro zobrazeni v tkinter
        mon =  monochromeim.resize((int(monochromeim.width*800/monochromeim.height), 800))
        col = colourim.resize((int(monochromeim.width*800/monochromeim.height), 800))
        monochromeim = ImageTk.PhotoImage(mon)
        colourim = ImageTk.PhotoImage(col)

        root.title("Image Viewer")
        root.geometry("800x900")

        ### vytvori a zobrazi rozhrani
        label = Label(image=monochromeim)
        label.grid(row=1, column=0, columnspan=4) 
        button_mono = Button(root, text="Monochrome", command=lambda: self.setImage(monochromeim))
        button_exit = Button(root, text="Exit", command=root.quit)
        button_col = Button(root, text="Colour", command=lambda: self.setImage(colourim))
        button_mono.grid(row=5, column=0)
        button_exit.grid(row=5, column=1)
        button_col.grid(row=5, column=2)

        root.mainloop()

    def setImage(self, img):
        """
        Sets image to be displayed
        """

        label = Label(image=img)
        label.grid(row=1, column=0, columnspan=4)