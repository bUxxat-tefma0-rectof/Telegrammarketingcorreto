import qrcode
from io import BytesIO
from aiogram.types import BufferedInputFile

def generate_qr_image(qr_text: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    bio = BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    return BufferedInputFile(bio.getvalue(), filename="qrcode.png")
