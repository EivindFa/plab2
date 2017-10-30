import os
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageDraw
import random


class Warhol:

    def __init__(self):
        self.path = "images\\"
        self.images_list = os.listdir(self.path)

        self.pixel_colors = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'white': (255, 255, 255),
                         'black': (0, 0, 0)}


    def load_image(self, infile):
        fn, ext = os.path.splitext(infile)
        outfile = fn + ".jpeg"
        image = None
        try:
            image = Image.open(self.path + outfile)
        except IOError:
            print("Cannot convert ", infile)
        return image

    def blur(self, image, value):
        return image.filter(ImageFilter.GaussianBlur(value))

    def rotate(self, image, degrees):
        return image.rotate(degrees)

    def dump_image(self, image, name):
        image.save(self.path + name + '.jpeg')

    def display(self, image):
        image.show()

    def resize(self, image, new_size):
        return image.resize(new_size)

    def scale(self, image, x_factor, y_factor):
        return image.resize((round(x_factor)*image.size[0], round(y_factor)*image.size[1]))

    def change_contrast(self, image, factor):
        enh = ImageEnhance.Contrast(image)
        return enh.enhance(factor)

    def make_sharper(self, image, factor):
        enh = ImageEnhance.Sharpness(image)
        return enh.enhance(factor)

    def invert_colors(self, image):
        return ImageOps.invert(image)

    def flip(self, image):
        return ImageOps.flip(image)

    def make_gray(self, image):
        return ImageOps.grayscale(image)

    def draw(self,coordinates, fill, width):
        return ImageDraw.ImageDraw.line(coordinates, fill, width)

    def is_bigger(self, image1, image2):
        return image1.size[0] > image2.size[0] or image1.size[1] > image2.size[1]

    def paste(self, back_image, front_image, x, y):
        copy = back_image
        copy.paste(front_image, (x, y))
        return copy

    def get_image_dims(self, image):
        return image.size[0], image.size[1]

    def get_pixel(self, image, x, y):
        return image.getpixel((x, y))

    def set_pixel(self, image, x, y, rgb):
        image.putpixel((x, y), rgb)
        return image

    def replace_random_pixels(self, image):
        xrange = image.size[0] - 1
        yrange = image.size[1] - 1
        #new = image
        colors = ['red', 'green', 'blue', 'white', 'black']
        for a in range(0, yrange*xrange):
            x = random.randint(0, xrange)
            y = random.randint(0, yrange)
            i = random.randint(0, 4)
            color = colors[i]
            image = self.set_pixel(image, x, y, self.pixel_colors[color])
        return image

    def remove_color(self, image, color):
        xrange = image.size[0]
        yrange = image.size[1]
        new = Image.new('RGB', (image.size[0], image.size[1]))
        if color == 'red':
            i = 0
        elif color == 'green':
            i = 1
        else:
            i = 2
        for x in range(xrange):
            for y in range(yrange):
                p = self.get_pixel(image, x, y)
                if p[i] != 0:
                    l = list(p)
                    l[i] = 0
                    self.set_pixel(new, x, y, tuple(l))
        return new


    def combine_pixels(self, p1, p2, alpha):
        rgb = [0,0,0]
        for i in range(3):
            rgb[i] = round(p1[i]*alpha + p2[i]*(1-alpha))
        return tuple(rgb)

    def morph(self, image1, image2, alpha):
        new = Image.new('RGB', (image1.size[0], image1.size[1]))
        for x in range(new.size[0]):
            for y in range(new.size[1]):
                rgb = self.combine_pixels(self.get_pixel(image1, x, y), self.get_pixel(image2, x, y), alpha)
                self.set_pixel(new, x, y, rgb)
        return new

    def morph3(self, image1, image2):
        im1 = self.morph(image1, image2, 1.00)
        im2 = self.morph(image1, image2, 0.80)
        im3 = self.morph(image1, image2, 0.60)
        im4 = self.morph(image1, image2, 0.20)
        im5 = self.morph(image1, image2, 0.00)
        return im1, im2, im3, im4, im5


def main():
    artist = Warhol()
    image1 = artist.load_image("campus.gif")
    image2 = artist.load_image("donaldduck.jpeg")
    image3 = artist.load_image("einstein.jpeg")


    # Første bilde skal være bakerst
    image1 = artist.resize(image1, (1200, 900))
    copy = Image.new('RGB', (image1.size[0], image1.size[1]))  # Kopi til senere bruk
    copy = artist.paste(copy, image1, 0, 0)

    # Andre bilde skal plasseres i hjørnene til første bilde
    # Det skal roteres 45 deretter 90 grader med klokka, og redigeres på ulik måte for hvert hjørne
    # I tillegg morpher jeg bilde 4 ganger med image3 og plasserer det ett hakk inn mot midten for hver gang

    #  Finner passende størrelse på image2 og image3 basert på størrelsen til image1
    x_size = image1.size[0]//5
    y_size = image1.size[1]//5
    image2 = artist.resize(image2, (x_size, y_size))
    image3 = artist.resize(image3, (x_size, y_size))
    image1_xsize = artist.get_image_dims(image1)[0]  # Bredden på image1
    image1_ysize = artist.get_image_dims(image1)[1]  # Høyden på image1
    image2_xsize = artist.get_image_dims(image2)[0]  # Bredden på image2
    image2_ysize = artist.get_image_dims(image2)[1]  # Høyden på image2

    image2 = artist.rotate(image2, -45)  # Starter med det originale image2-bildet
    mi = artist.morph3(image2, image3)
    xstart = image1_xsize - image2_xsize
    ystart = 0
    for im in mi:
        image1 = artist.paste(image1, im, xstart, ystart)
        xstart -= x_size//2
        ystart += y_size//2

    image2 = artist.change_contrast(image2, 3)  # Øker kontrastene
    image2 = artist.rotate(image2, -90)
    mi = artist.morph3(image2, image3)
    xstart = image1_xsize - image2_xsize
    ystart = image1_ysize - image2_ysize
    for im in mi:
        image1 = artist.paste(image1, im, xstart, ystart)
        xstart -= x_size // 2
        ystart -= y_size // 2

    image2 = artist.invert_colors(image2)  # Inverterer fargene
    image2 = artist.rotate(image2, -90)
    mi = artist.morph3(image2, image3)
    xstart = 0
    ystart = image1_ysize - image2_ysize
    for im in mi:
        image1 = artist.paste(image1, im, xstart, ystart)
        xstart += x_size // 2
        ystart -= y_size // 2

    image2 = artist.blur(image2, 3)  # Gjør bilde mer utydelig
    image2 = artist.rotate(image2, -90)
    mi = artist.morph3(image2, image3)
    xstart = 0
    ystart = 0
    for im in mi:
        image1 = artist.paste(image1, im, xstart, ystart)
        xstart += x_size // 2
        ystart += y_size // 2


    # Redigerer liten versjon av image1 på 4 forskjellige måter
    # Plasserer de på ledig plass i stor versjon av image1
    new = artist.resize(copy, (x_size, y_size))
    sharpened = artist.make_sharper(new, 10)  # Gjør bilde skarpere
    image1 = artist.paste(image1, sharpened, image1.size[0]//2 - new.size[0]//2, 0)

    red_removed = artist.remove_color(new, 'red')  # Fjerner all rødfarge
    image1 = artist.paste(image1, red_removed, image1.size[0] - new.size[0],
                          image1.size[1] // 2 - new.size[1] // 2)

    gray = artist.make_gray(new)  # Gjør bilde svart/hvitt
    image1 = artist.paste(image1, gray, image1.size[0]//2 - new.size[0]//2,
                          image1.size[1] - new.size[1])

    draw_object = ImageDraw.Draw(new)  # Tegner en trekant vha. ImageDraw
    t1_coo = [(0, new.size[1]//4), (new.size[0], new.size[1]//4), (new.size[0]//2, new.size[1]), (0, new.size[1]//4)]
    t2_coo = [(new.size[0]//2, 0), (new.size[0], new.size[1]-new.size[1]//4), (0, new.size[1]-new.size[1]//4), (new.size[0]//2, 0)]
    draw_object.line(t1_coo, artist.pixel_colors['red'], 2)
    draw_object.line(t2_coo, artist.pixel_colors['red'], 2)
    image1 = artist.paste(image1, new, 0, image1.size[1] // 2 - new.size[1] // 2)

    # Tilslutt vises resultatet
    artist.display(image1)

main()