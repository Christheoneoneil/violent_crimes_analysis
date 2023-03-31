import os
import cv2
import pytesseract
from pdfminer.high_level import extract_text
from PIL import Image
from pdf2image import convert_from_path

# define pdf path
pdf_path = 'Atchison_note_1.pdf'                # change to desired pdf

# extract text
text = extract_text(pdf_path)

# define folder path
pdf_image_dir = '/filepath'                     # change to filepath
if not os.path.exists(pdf_image_dir):
    os.makedirs(pdf_image_dir)

# save separate pages of pdf as separate images
pages = convert_from_path(pdf_path, dpi=300)
for i, page in enumerate(pages):
    page.save(os.path.join(pdf_image_dir, f'page_{i}.png'), 'PNG')

# identify handwritten text
handwritten_text = []
for page_image_path in os.listdir(pdf_image_dir):
    image_path = os.path.join(pdf_image_dir, page_image_path)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilate = cv2.dilate(thresh, kernel, iterations=5)
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        roi = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)

        # append handwritten text to list
        handwritten_text.append(text)
