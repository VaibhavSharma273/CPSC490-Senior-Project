import sys
import os

picdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/pic'
libdir = '/home/vaibhavsharma/Downloads/bcm2835-1.71/WiringPi/OLED_Module_Code/OLED_Module_Code/RaspberryPi/python/lib'
sys.path.append(libdir)

from waveshare_OLED import OLED_1in51
from PIL import Image,ImageDraw,ImageFont
import logging  
import time
import traceback
from googletrans import Translator
import pytesseract
import os
from gtts import gTTS
from picamera import PiCamera
import util

# Filename of the image
FILENAME = "text"
# Button pin
BUTTON_PIN = 10

# Create a Translator object
translator = Translator()

# Create a camera object
camera = PiCamera()
camera.resolution = (1024, 768)


def button_callback(channel):

    print("Button was pushed! Capturing image now.")

    # STEP 1: Capture image
    camera.start_preview()
    camera.capture(FILENAME + '.jpeg')

    # STEP 2: Open image
    original_image = util.get_image(FILENAME + '.jpeg')

    # STEP 2: Preprocess image
    processed_image = util.preprocess_image(original_image)

    # STEP 3: Run OCR
    ocr_text = util.run_ocr_regular(processed_image)

    # STEP 4: Clean up text
    processed_text = util.remove_whitespace(ocr_text)

    # STEP 5: Translate text
    if processed_text:
        translated_text = translator.translate(processed_text, dest='hi').text
        print('Original text: ', text)
        print('Translated text: ', translated_text)

        # STEP 6: Convert text to speech and output
        util.convert_text_to_speech_hindi(translated_text)
        util.play_audio()

        # STEP 7: Send to display
        util.output_display(translated_text)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(BUTTON_PIN,GPIO.RISING,callback=button_callback)

GPIO.cleanup()

button_callback()
