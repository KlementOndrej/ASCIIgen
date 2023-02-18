from PIL import Image, ImageDraw

class ImageToConvert:
    charset = {
        "default": "@#&O*^+~-,. ",
        "reverse": " .,-~+^*O&#@",
        "long": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1[]",
        "short": "#. "
    }

    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file
        self.input_image = Image.open(path_to_file).convert('RGB') #nahraje obrazek a zajisti ze je v rgb
        self.input_image.resize((int(self.input_image.width), int(self.input_image.height*(10/18)))) #zmeni pomer stran aby kompenzoval rozmery znaku
        self.ascii_text = ""
    
    ### skaluje obrazek
    def scale(self, scale_factor: float):
        self.input_image = self.input_image.resize((int(scale_factor*self.input_image.width), int(scale_factor*self.input_image.height*(10/18))))   
                                                        #zmeni rozmery podle zadaneho pomeru
        
    ### vezme intenzitu barvy a urci ji znak ktery ji ma reprezentovat
    def pickChar(self, ipt: int, chset: str = "default"):
        characters = list(self.charset[chset])          #nahraje charset
        char_length = len(characters)
        interval = char_length/256                      #urci interval podle ktereho se stupnuji barvy
        output = characters[int(ipt*interval)]          #vezme na zacatku zadanou intenzitu barvy a urci ji vhodny znak
        return output

    ### prevede obrazek na text
    def imageToText(self, chset: str = "default"):
        image_pix = self.input_image.load()                 #nahraje pixely obrazku
        print(self.input_image.width, self.input_image.height)
        for y in range(self.input_image.height):            #postupne jde po radkach pixelu
            for x in range(self.input_image.width):
                r, g, b = image_pix[x, y]                   #zjisti barvu pixelu
                c = int(r/3 + g/3 + b/3)                    #zprumeruje intenzitu barvy
                self.ascii_text = self.ascii_text + self.pickChar(c, chset)     #prida znak, urceny na zaklade intenzity, do retezce
            self.ascii_text = self.ascii_text + "\n"                    #na konci radku pixelu udela novou radku v textu

    ### generuje orazek z textu
    def textToImage(self):
        if self.ascii_text == "":
            print("This image was not yet converted to text")
            return
        output_image = Image.new('RGB', (int(self.input_image.width*10), int(self.input_image.height*18)), 'black') 
                                                        #vytvori novy obrazek
        i = 0
        for c in self.ascii_text:                       #projde vsechny znaky v textu
            ImageDraw.Draw(output_image).text(((i%(self.input_image.width+1))*10+2, int(i/(self.input_image.width+1))*18+2), c)
                                                        #nakresli do obrazku znak
            i = i + 1
        return output_image

    ### generuje obrazek slozeny z barevnych znaku
    def imageToColorImage(self, chset: str = "default"):
        output_image = Image.new('RGB', (int(self.input_image.width*10), int(self.input_image.height*18)), 'white') 
                                                        #vytvori novy obrazek s puvodnim pomerem stran      
        image_pix = self.input_image.load()                  #nahraje pixely obrazku
        for y in range(self.input_image.height):                   #postupne jde po radkach pixelu
                for x in range(self.input_image.width):
                    r, g, b = image_pix[x, y]           #zjisti barvu pixelu
                    c = int(r/3 + g/3 + b/3)            #zprumeruje intenzitu barvy
                    ImageDraw.Draw(output_image).text((x*10+2, y*18+2), self.pickChar(c, chset), fill=(r, g, b))
                                                        #nakresli do obrazku znak urceny na zaklad intenzity a s puvodeni barvou pixelu
        return output_image

if __name__ == "__main__":
    im = ImageToConvert("test.jpeg")
    im.scale(0.01)
    im.imageToText("reverse")
    print(im.ascii_text)
    im.textToImage().save("output.png")
    im.imageToColorImage().save("Out.png")