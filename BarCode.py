# import EAN13 from barcode module
from barcode import EAN13, EAN14
import hashlib
import barcode

# import ImageWriter to generate an image file
from barcode.writer import ImageWriter

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

    code = barcode.get('code128', data, writer=ImageWriter())

    # Save the barcode to an image file
    code.save(filename+'_bar')