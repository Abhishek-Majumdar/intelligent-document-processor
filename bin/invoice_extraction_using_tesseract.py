from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os
import time

start_time = time.time()
print("Invoice extraction started at : " + str(start_time))

possible_values_for_total = ['Total Amount Paid', 'Balance Due']
  
# Path of the pdf 
PDF_file = "path/to/pdf_invoice"

# Creating a text file to write the output 
outfile = "path/to/output_text_file"

#Creating path to tesseract binary
pytesseract.pytesseract.tesseract_cmd = r'path/to/tesseract_binary' 
    
''' 
Part #1 : Converting PDF to images 
'''
  
# Store all the pages of the PDF in a variable 
pages = convert_from_path(PDF_file, 500) 
  
# Counter to store images of each page of PDF to image 
image_counter = 1
  
# Iterate through all the pages stored above 
for page in pages: 
  
    # Declaring filename for each page of PDF as JPG 
    # For each page, filename will be: 
    # PDF page 1 -> page_1.jpg 
    # PDF page 2 -> page_2.jpg 
    # PDF page 3 -> page_3.jpg 
    # .... 
    # PDF page n -> page_n.jpg 
    filename = "page_"+str(image_counter)+".jpg"
    # Save the image of the page in system 
    page.save(filename, 'JPEG') 
  
    # Increment the counter to update filename 
    image_counter = image_counter + 1

print("Number of pages detected in PDF : " + str(image_counter -1))
    
''' 
Part #2 - Recognizing text from the images using OCR 
'''
# Variable to get count of total number of pages 
filelimit = image_counter-1

  
# Open the file in append mode so that  
# All contents of all images are added to the same file 
#f = open(outfile, "a") 
text = '' 
    
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 
  
    # Set filename to recognize text from 
    # Again, these files will be: 
    # page_1.jpg 
    # page_2.jpg 
    # .... 
    # page_n.jpg 
    filename = "page_"+str(i)+".jpg"
    # Recognize the text as string in image using pytesserct 
    tesseract_start_time = time.time()
    print("Tesseract extraction started at : " + str(start_time))
    text = text + str(((pytesseract.image_to_string(Image.open(filename))))) 
    print("Time taken to process image " + filename + " : " + str(time.time() - tesseract_start_time))
  
# The recognized text is stored in variable text 
# Any string processing may be applied on text 
# Here, basic formatting has been done: 
# In many PDFs, at line ending, if a word can't 
# be written fully, a 'hyphen' is added. 
# The rest of the word is written in the next line 
# Eg: This is a sample text this word here GeeksF- 
# orGeeks is half on first line, remaining on next. 
# To remove this, we replace every '-\n' to ''. 
text = text.replace('-\n', '')
#print("Extracted text with tesseract : " + text)
    
lines = text.split('\n')
print('Number of lines in invoice : ' + str(len(lines)))

for line in lines:
    if ':' in line and any(total_mark in line for total_mark in possible_values_for_total):
        print('Invoice total : ' + line.split(':')[1])
  
# Finally, write the processed text to the file. 
#f.write(text) 
  
# Close the file after writing all the text. 
#f.close() 

print("Process completed in : " + str(time.time() - start_time))
print(text)