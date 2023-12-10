from gtts import gTTS
import cv2
# from matplotlib import pyplot as plt
import pytesseract
import numpy as np
import os

# ------------ Pre-processing strategies
def get_image(file):
    return cv2.imread(file)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def recale(image):
    return cv2.resxize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

def remove_noise(image):
    return cv2.medianBlur(image,5)

def gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def normalize(image):
    img = cv2.normalize(img, np.zeros((img.shape[0], img.shape[1])), 0, 255, cv2.NORM_MINMAX)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

def distance_transform(image):
    dist = cv2.distanceTransform(image, cv2.DIST_L2, 5)
    dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")
    dist = cv2.threshold(dist, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return dist

def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# get bounding boxes
def get_bounding_boxes(image):
    h, w, c = image.shape
    boxes = pytesseract.image_to_boxes(image) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)

# use bounding boxes for recognition
def use_bounding_boxes(image):
    results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT) 
    final = []
    for i in range(0, len(results["text"])):
        x = results["left"][i]
        y = results["top"][i]

        w = results["width"][i]
        h = results["height"][i]

        text = results["text"][i]
        conf = int(results["conf"][i])

        if conf > 70:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, text, (x, y - 10))
            final.append(text)
                        
    cv2.imshow('img', image)
    cv2.waitKey(0)
    return final

# ------------ Pre-processing
# Single Strategy
def preprocess_image(image):
    img = get_grayscale(image)
    img = recale(img)
    img = remove_noise(img)
    img = opening(img)
    img = thresholding(img)

    return img

# Combined Stratgies -- Only for testing and displaying output
# def plot_image_grid(images, nrows, ncols, cmap='gray'):
#     '''Plot a grid of images'''
#     imgs = [images[i][0] if len(images) > i else None for i in range(nrows * ncols)]
#     titles = [images[i][1] if len(images) > i else None for i in range(nrows * ncols)]
#     texts = [images[i][2] if len(images) > i else None for i in range(nrows * ncols)]

#     f, axes = plt.subplots(nrows, ncols, figsize=(3*ncols, 2*nrows))
#     axes = axes.flatten()[:len(imgs)]
#     for i in range(len(imgs)): 
#         ax = axes[i]
#         ax.imshow(imgs[i], cmap=cmap)
#         ax.set_title(titles[i], size="10")
#         ax.text(0.5,-0.5, texts[i], size=8, ha="center", transform=ax.transAxes)
#         ax.axis('off')

# def preprocess_image_grid(image):
#     # Array of images
#     images = []

#     # Original Image
#     images.append([image, "Original Image", run_ocr(image)])

#     # Grayscale Image
#     gray = get_grayscale(image)
#     images.append([gray, "Grayscale Image", run_ocr(gray)])

#     # De-noise Image
#     img = remove_noise(gray)
#     images.append([img, "Noise Removal", run_ocr(img)])

#     # Thresholding
#     img = thresholding(gray)
#     images.append([img, "Thresholding", run_ocr(img)])

#     # Canny
#     img = canny(gray)
#     images.append([img, "Canny", run_ocr(img)])

#     # Deskewed
#     img = deskew(gray)
#     images.append([img, "Deskwed", run_ocr(img)])

#     # Erosion
#     img = erode(gray)
#     images.append([img, "Erosion", run_ocr(img)])

#     # Dilation
#     img = dilate(gray)
#     images.append([img, "Dilation", run_ocr(img)])
        
#     # Opening
#     img = opening(gray)
#     images.append([img, "Opening", run_ocr(img)])

#     # custom_config = r'--oem 3 --psm 6'
#     # pytesseract.image_to_string(img, config=custom_config)

#     plot_image_grid(images, 3, 3)
#     plt.subplots_adjust(hspace=1)
#     plt.axis('off')
#     plt.show()

# ------------ OCR
# PyTesseract Text Detection 
def run_ocr(image):
    custom_config = r'--psm 6' # single uniform block
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# PyTesseract Text Detection Default
def run_ocr_regular(image):
    text = pytesseract.image_to_string(image)
    return text

def run_ocr_bounding_boxes(image):
    text = pytesseract.image_to_string(image)
    return text

# ------------ Clean up text
def remove_whitespace(text):
    return ' '.join(text.split())

# ------------  Output
def convert_text_to_speech_hindi(text):
    myobj = gTTS(text=text, lang='hi', slow=False) 
    myobj.save("text.mp3") 

def output_audio(filename):
    os.system("mpg123 " + "-q " + "text.mp3")

def output_display(translated_text):
    try:
        disp = OLED_1in51.OLED_1in51()

        logging.info("\r1.51inch OLED ")
        # Initialize library.
        disp.Init()
        # Clear display.
        logging.info("clear display")
        disp.clear()

        # Create blank image for drawing.
        image1 = Image.new('1', (60, 60), "WHITE")
        draw = ImageDraw.Draw(image1)
        font2 = ImageFont.truetype(os.path.join(picdir, 'AksharUnicode.ttf'), 24)
        logging.info ("***draw text")
        draw.text((0,0), translated_text, font = font2, fill = 0)
        image1 = image1.rotate(90) 
        disp.ShowImage(disp.getbuffer(image1))
        time.sleep(3) 
        disp.clear()

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        OLED_1in51.config.module_exit()
        exit()
