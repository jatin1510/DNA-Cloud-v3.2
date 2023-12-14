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
from barcode import generate
from barcode.writer import ImageWriter 
from PIL import PngImagePlugin
from PIL import ImageFont
import os

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
    try:
        code128 = barcode.get_barcode_class('code128')
        code = code128(data, writer=ImageWriter())

        # Save the barcode to an image file
        _ = code.save(filename+'_bar')
    except Exception as e:
        print(e)