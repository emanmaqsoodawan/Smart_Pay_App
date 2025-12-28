import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transaction_controller import TransactionController

class TestTransactionController(unittest.TestCase):

    @patch('transaction_controller.DBConnection.get_connection')
    def test_add_transaction(self, mock_get_conn):
        """Test adding a transaction."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        success, message = TransactionController.add_transaction(1, 1, 100.0, "Income", "2023-01-01")
        
        self.assertTrue(success)
        self.assertEqual(message, "Transaction added successfully")
        mock_conn.commit.assert_called_once()

    @patch('transaction_controller.DBConnection.get_connection')
    def test_get_balance(self, mock_get_conn):
        """Test calculating user balance."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock return value: TotalIncome=1000, TotalExpense=200
        mock_cursor.fetchone.return_value = (1000.0, 200.0)
        
        balance = TransactionController.get_balance(1)
        
        self.assertEqual(balance, 800.0)

    @patch('transaction_controller.DBConnection.get_connection')
    def test_process_transfer(self, mock_get_conn):
        """Test money transfer between users."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock category IDs
        mock_cursor.fetchone.side_effect = [
            (10,), # Sent Category
            (11,), # Received Category
            ("Alice",), # Sender Name
            ("Bob",)    # Receiver Name
        ]
        
        success, message = TransactionController.process_transfer(1, 2, 500.0, "2023-01-01")
        
        self.assertTrue(success)
        self.assertEqual(message, "Transfer successful")
        # Should call execute 4 times (2 category lookups, 2 user lookups, 2 inserts = 6 actually? wait side_effect)
        # The logic does: 2 cat lookups, 2 user lookups, 2 inserts.
        # My side_effect only covers the first 4 fetchone calls.
        # The Inserts don't use fetchone.
        self.assertTrue(mock_cursor.execute.call_count >= 6)
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
