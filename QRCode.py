import qrcode

def generateQR(data, filename):
    # Generate a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an Image object from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code as an image file
    img.save(filename + "_qr.png")