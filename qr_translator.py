import qrcode
from IPython.display import display

# The link you want to encode
url = "https://uttyler.instructure.com/"

# Create a QR code object
qr = qrcode.QRCode(
    version=1,  # Controls size of QR code (1 is smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=16,  # Size of each box in pixels
    border=4,  # Thickness of border
)

qr.add_data(url)
qr.make(fit=True)

# Generate the image
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("my_qr_code.png")
display(img)

print("QR code saved as my_qr_code.png")