from db_connection import DBConnection
import pyodbc
import random

def generate_account_number():
    # Generate 10 digit number string
    return str(random.randint(1000000000, 9999999999))

def update_schema():
    conn = DBConnection.get_connection()
    if not conn:
        print("Connection failed.")
        return

    cursor = conn.cursor()
    
    # 1. Check if column exists
    try:
        cursor.execute("SELECT account_number FROM Users")
        print("Column 'account_number' already exists.")
    except:
        print("Column 'account_number' missing. Adding it...")
        try:
            # Add column (nullable first to allow existing records)
            cursor.execute("ALTER TABLE Users ADD account_number NVARCHAR(20)")
            conn.commit()
            print("Column added.")
        except Exception as e:
            print(f"Error adding column: {e}")
            return

    # 2. Backfill existing users (Generate random numbers)
    try:
        cursor.execute("SELECT user_id FROM Users WHERE account_number IS NULL")
        rows = cursor.fetchall()
        
        for row in rows:
            uid = row[0]
            acc_num = generate_account_number()
            cursor.execute("UPDATE Users SET account_number = ? WHERE user_id = ?", (acc_num, uid))
            print(f"Assigned Account Num {acc_num} to User ID {uid}")
        
        conn.commit()
    except Exception as e:
        print(f"Error backfilling data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema()
