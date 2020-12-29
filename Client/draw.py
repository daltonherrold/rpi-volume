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
    font = ImageFont.truetype("/home/pi/rpi-volume/Client/helvetica.ttf", 13)
    return draw, disp, font, image


def draw_process(draw, disp, font, image, process, pos):
    # Get out the things that we need
    name = process['name'].split(".")[0].capitalize()
    volume = process['volume']

    # Set up our positions
    width = disp.width - 25
    height = disp.height

    draw.rectangle((0,0,width+25,height), outline=0, fill=0)
    # draw.text(((image.size[0]-text_size[0])/2, 1), name, font=font, fill=255)
    
    # Draw the three text fields that we have on the screen
    draw.text((3, -1), name, font=font, fill=255)
    text_size = draw.textsize(str(round(volume*100)), font)
    draw.text((image.size[0]-text_size[0], 17), str(round(volume*100)), font=font, fill=255)
    text_size = draw.textsize(pos, font)
    draw.text((image.size[0]-text_size[0], -1), pos, font=font, fill=255)
    
    # Draw the volume slider
    draw.rectangle((3, 19, width-3, height-1), outline=255, fill=0)
    new_width = (width-3)*volume if (width-3)*volume >=3 else 3
    draw.rectangle((3, 19, new_width, height-1), outline=255, fill=255)

    # Display the image
    disp.image(image)
    disp.display()


