import barcode
from barcode.writer import ImageWriter

def generate_barcode(data, barcode_type='code128', output_path='barcode'):
    # Generate the barcode
    code = barcode.get(barcode_type, data, writer=ImageWriter())

    # Save the barcode to an image file
    filename = f"{output_path}_{barcode_type}_{data}"
    code.save(filename)

    print(f"Barcode saved as {filename}")

# Example usage
data_to_encode = "Hello1111111123"
generate_barcode(data_to_encode)
