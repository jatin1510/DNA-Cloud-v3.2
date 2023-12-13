"""
##########################################################################################
Improvised Version: DNA Cloud 3.2
Developers: Jaimin Satani, Jatin Ranpariya, Devarshi Joshi, Arpan Singhala, Chaitri Gudhka, Mukund Ladani, Nikhil Vaghasiya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file will run on python 3.10.5
##########################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
##########################################################################################
"""

import hashlib
import barcode
import os
import aspose.words as aw

def svgToPng(fileName, filepath):

    # create a document
    doc = aw.Document()

    # create a document builder and initialize it with document object
    builder = aw.DocumentBuilder(doc)

    # insert SVG image to document
    shape = builder.insert_image(fileName)

    # OPTIONAL
    # Calculate the maximum width and height and update page settings 
    # to crop the document to fit the size of the pictures.
    pageSetup = builder.page_setup
    pageSetup.page_width = shape.width
    pageSetup.page_height = shape.height
    pageSetup.top_margin = 0
    pageSetup.left_margin = 0
    pageSetup.bottom_margin = 0
    pageSetup.right_margin = 0

    # save as PNG
    doc.save(filepath + ".png")    

def hash_to_13_digits(number):
    # Convert the number to a string
    number_str = str(number)

    # Use SHA-256 hash function
    hash_object = hashlib.sha256(number_str.encode())

    # Get the hexadecimal digest of the hash and convert it to an integer
    hash_int = int(hash_object.hexdigest(), 16)

    # Take the last 13 digits of the hash and return as a string
    result = str(hash_int)[-13:]

    return result

def generateBarcode(data, filename):

    code128 = barcode.get_barcode_class('code128')
    code = code128(data)

    # Save the barcode to an image file
    code.save(filename+'_bar')
    
    svgToPng(filename+'_bar.svg', filename)
    os.remove(filename+'_bar.svg')