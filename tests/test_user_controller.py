import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user_controller import UserController

class TestUserController(unittest.TestCase):

    @patch('user_controller.DBConnection.get_connection')
    def test_register_user_success(self, mock_get_conn):
        """Test successful user registration."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock fetchone to return None (user doesn't exist)
        mock_cursor.fetchone.return_value = None
        
        success, message = UserController.register_user("newuser", "password123")
        
        self.assertTrue(success)
        self.assertIn("User registered successfully", message)
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('user_controller.DBConnection.get_connection')
    def test_register_user_username_exists(self, mock_get_conn):
        """Test registration when username already exists."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock fetchone to return a row (user exists)
        mock_cursor.fetchone.return_value = (1,)
        
        success, message = UserController.register_user("existinguser", "password123")
        
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
        mock_conn.commit.assert_not_called()

    @patch('user_controller.DBConnection.get_connection')
    def test_login_user_success(self, mock_get_conn):
        """Test successful login."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock fetchone to return user data
        mock_cursor.fetchone.return_value = (1, "testuser", "1234567890")
        
        user_data, message = UserController.login_user("testuser", "password")
        
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['username'], "testuser")
        self.assertEqual(message, "Login successful")

    @patch('user_controller.DBConnection.get_connection')
    def test_login_user_failure(self, mock_get_conn):
        """Test login failure."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock fetchone to return None
        mock_cursor.fetchone.return_value = None
        
        user_data, message = UserController.login_user("wronguser", "password")
        
        self.assertIsNone(user_data)
        self.assertEqual(message, "Invalid username or password")

if __name__ == '__main__':
    unittest.main()
