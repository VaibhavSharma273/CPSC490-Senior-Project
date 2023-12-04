import RPi.GPIO as GPIO 
import time

def button_callback(channel):
    print("Button was pushed!")
    time.sleep(1)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 31 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(31,GPIO.RISING,callback=button_callback) # Set up event on pin 31 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up