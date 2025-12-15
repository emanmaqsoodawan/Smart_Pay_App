from db_connection import DBConnection
import pyodbc

class UserController:
    @staticmethod
    @staticmethod
    def register_user(username, password):
        conn = DBConnection.get_connection()
        if not conn:
            return False, "Database connection failed"
        
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Username already exists"

            # Generate Account Number
            import random
            account_number = str(random.randint(1000000000, 9999999999))

            # Insert new user
            cursor.execute("INSERT INTO Users (username, password, account_number) VALUES (?, ?, ?)", (username, password, account_number))
            conn.commit()
            return True, f"User registered successfully! Account #: {account_number}"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def login_user(username, password):
        conn = DBConnection.get_connection()
        if not conn:
            return None, "Database connection failed"
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id, username, account_number FROM Users WHERE username = ? AND password = ?", (username, password))
            row = cursor.fetchone()
            
            if row:
                return {"user_id": row[0], "username": row[1], "account_number": row[2]}, "Login successful"
            else:
                return None, "Invalid username or password"
        except Exception as e:
            return None, str(e)
        finally:
            conn.close()

    @staticmethod
    def get_user_id_by_username(username):
        conn = DBConnection.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
        except:
            return None
        finally:
            conn.close()
