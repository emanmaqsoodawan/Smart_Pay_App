import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import generate_qr_code, generate_pdf_receipt

class TestUtils(unittest.TestCase):
    
    def test_generate_qr_code(self):
        """Test if QR code generation returns a PIL image object."""
        data = "Test QR Data"
        img = generate_qr_code(data)
        # Check if it has a 'save' method which indicates it's a PIL image
        self.assertTrue(hasattr(img, 'save'))
        self.assertTrue(hasattr(img, 'size'))

    @patch('utils.FPDF')
    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_generate_pdf_receipt(self, mock_exists, mock_makedirs, mock_fpdf):
        """Test PDF receipt generation with mocked FPDF."""
        # Setup mocks
        mock_exists.return_value = False # Simulate directory doesn't exist
        
        mock_pdf_instance = MagicMock()
        mock_fpdf.return_value = mock_pdf_instance
        
        transaction_details = {
            'id': 123,
            'sender': 'Alice',
            'receiver': 'Bob',
            'amount': 500.0,
            'date': '2023-10-27'
        }
        
        path = generate_pdf_receipt(transaction_details)
        
        # Verify FPDF calls
        mock_pdf_instance.add_page.assert_called_once()
        mock_pdf_instance.cell.assert_called()
        mock_pdf_instance.output.assert_called()
        
        # Verify directory creation
        mock_makedirs.assert_called_with("receipts")
        
        # Verify return path
        self.assertTrue(path.endswith("receipt_123.pdf"))

if __name__ == '__main__':
    unittest.main()
