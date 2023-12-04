import sys
import os

# Configuring paths for display libraries
picdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/pic'
libdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/lib'

sys.path.append('/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/lib')

from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
import logging  
import time
import traceback
from googletrans import Translator

logging.basicConfig(level=logging.INFO)
translator = Translator()

try:
    disp = OLED_1in51.OLED_1in51()

    logging.info("\r1.51inch OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

    # Sample text
    text = "Hello!"
    translated_text = translator.translate(text, dest='hi').text
    print('Original text: ', text)
    print('Translated text: ', translated_text)

    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font2 = ImageFont.truetype(os.path.join(picdir, 'AksharUnicode.ttf'), 24)
    logging.info ("***draw line")
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,0),(0,63)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
    logging.info ("***draw text")
    draw.text((20,0), text, font = font1, fill = 0)
    draw.text((20,24), translated_text, font = font2, fill = 0)
    image1 = image1.rotate(180) 
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(3) 
    disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    OLED_1in51.config.module_exit()
    exit()