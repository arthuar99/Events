import os
import qrcode
from app.core.config import settings

# Create QR directory if it doesn't exist
QR_DIR = os.path.join(os.getcwd(), "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)

def generate_qr_code(ticket_url_or_token: str, filename: str) -> str:
    """
    Generate a QR code for the given ticket URL or token and save it to a file.
    
    Args:
        ticket_url_or_token (str): The URL or token to encode in the QR code
        filename (str): The filename (without extension) for the QR code image
        
    Returns:
        str: The path to the saved QR code image
        
    Raises:
        Exception: If there's an error generating or saving the QR code
    """
    try:
        # Generate QR code
        img = qrcode.make(ticket_url_or_token)
        
        # Create full path with .png extension
        path = os.path.join(QR_DIR, f"{filename}.png")
        
        # Save the QR code image
        img.save(path)
        
        return path
    except Exception as e:
        raise Exception(f"Failed to generate QR code: {str(e)}")