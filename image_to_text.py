import os
import cv2
import pytesseract
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path

'''Note: This script only works reliably on identifying on non-handwritten text.'''

def extract_handwritten_text(pdf_path, output_file):
    # extract text
    text = extract_text(pdf_path)

    # check if PDF contains handwritten text
    if 'handwritten' not in text.lower():
        print('No handwritten text found in PDF.')
        return

    # save separate pages of pdf as separate images
    pages = convert_from_path(pdf_path, dpi=300)
    handwritten_text = []
    for i, page in enumerate(pages):
        # convert page to grayscale and save as temporary image file
        page_path = f'temp_page_{i}.png'
        page.save(page_path, 'PNG')
        img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)

        # identify handwritten text
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilate = cv2.dilate(thresh, kernel, iterations=5)
        contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            roi = img[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi)

            # append handwritten text to list
            handwritten_text.append(text)

        # delete temporary image file
        os.remove(page_path)

    # write handwritten text to output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(handwritten_text))
    
    print(f'Successfully extracted {len(handwritten_text)} instances of handwritten text.')


def extract_all_text(pdf_path, output_file):
    # extract text
    text = extract_text(pdf_path)

    # save separate pages of pdf as separate images
    pages = convert_from_path(pdf_path, dpi=300)
    all_text = []
    for i, page in enumerate(pages):
        # convert page to grayscale and save as temporary image file
        page_path = f'temp_page_{i}.png'
        page.save(page_path, 'PNG')
        img = cv2.imread(page_path, cv2.IMREAD_GRAYSCALE)

        # identify all text
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilate = cv2.dilate(thresh, kernel, iterations=5)
        contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            roi = img[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi)

            # append text to list
            all_text.append(text)

        # delete temporary image file
        os.remove(page_path)

    # write all text to output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(all_text))

    print(f'Successfully extracted {len(all_text)} instances of text.')


    

# Example of function use
pdf_path = 'Atchison_note_1.pdf'
output_file = 'Aitchison_note_1_text.txt'
extract_all_text(pdf_path, output_file)
