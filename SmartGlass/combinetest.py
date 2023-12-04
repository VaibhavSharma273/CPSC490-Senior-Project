# Button
import RPi.GPIO as GPIO 

# Camera
from picamera import PiCamera

import sys
import os

picdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/pic'
libdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/lib'

sys.path.append('/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/lib')

# Display
from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
import logging 
import time
import traceback

# Translator
from googletrans import Translator

# OCR
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

logging.basicConfig(level=logging.INFO)
translator = Translator()
camera = PiCamera()
camera.resolution = (1024, 768)

def button_callback(channel):
    print("Button was pushed!")
    camera.capture('sample.png')

    with Image.open('sample.png') as image:\
    im = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(im)
    filename = "temp.png"
    im.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    print(text)

    try:
        disp = OLED_1in51.OLED_1in51()
        logging.info("\r1.51inch OLED ")
        disp.Init()
        logging.info("clear display")
        disp.clear()

        text = "Hello!"
        translated_text = translator.translate(text, dest='hi').text

        image1 = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font2 = ImageFont.truetype(os.path.join(picdir, 'AksharUnicode.ttf'), 24)
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

    time.sleep(2)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

GPIO.add_event_detect(26,GPIO.RISING,callback=button_callback)
message = input("Press enter to quit\n") # Run until someone presses enter
GPIO.cleanup()
