import qrcode
from fpdf import FPDF
import os
from PIL import ImageTk, Image

def generate_qr_code(data):
    """
    Generates a QR code image for the given data.
    Returns a PIL Image object (convertible to ImageTk).
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(data))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def generate_pdf_receipt(transaction_details):
    """
    Generates a PDF receipt for a transaction.
    transaction_details: dict with keys (id, sender, receiver, amount, date)
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Smart Pay App - Transaction Receipt", ln=True, align='C')
    
    pdf.ln(20) # Line break

    # Details
    pdf.set_font("Arial", size=12)
    
    details = [
        f"Transaction ID: {transaction_details.get('id', 'N/A')}",
        f"Date: {transaction_details.get('date', 'N/A')}",
        f"Sender: {transaction_details.get('sender', 'N/A')}",
        f"Receiver: {transaction_details.get('receiver', 'N/A')}",
        f"Amount: Pkr {transaction_details.get('amount', 0):,.2f}",
        f"Status: COMPLETED"
    ]

    for line in details:
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Thank you for using Smart Pay App!", ln=True, align='C')

    # Save
    if not os.path.exists("receipts"):
        os.makedirs("receipts")
    
    filename = f"receipts/receipt_{transaction_details.get('id', 'temp')}.pdf"
    pdf.output(filename)
    return os.path.abspath(filename)
