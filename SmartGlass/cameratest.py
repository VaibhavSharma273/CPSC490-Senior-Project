from picamera import PiCamera
from time import sleep

camera = PiCamera() # Create PiCamera object
sleep(5)
camera.resolution = (1024, 768) # Specify resolution
camera.start_preview() 
camera.capture('sample.png') # Capture test image and save it in current directory as "sample.png"
