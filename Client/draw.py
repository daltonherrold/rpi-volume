import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def setup():
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
    disp.begin()
    disp.clear()
    disp.display()
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
    font = ImageFont.truetype("helvetica.ttf", 15)
    return draw, disp, font, image


def draw_process(draw, disp, font, image, process):
    name = process['name'].split(".")[0].capitalize()
    volume = process['volume']

    text_size = draw.textsize(name, font)
    width = disp.width
    height = disp.height

    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text(((image.size[0]-text_size[0])/2, 1), name, font=font, fill=255)
    draw.rectangle((3, 21, width-3, height-1), outline=255, fill=0)
    draw.rectangle((3, 21, (width-3)*volume, height-1), outline=255, fill=255)

    disp.image(image)
    disp.display()


