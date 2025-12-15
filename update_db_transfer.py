from db_connection import DBConnection
import pyodbc

def add_transfer_categories():
    conn = DBConnection.get_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    cursor = conn.cursor()
    categories = ['Transfer Sent', 'Transfer Received']

    print("Adding transfer categories...")
    for cat in categories:
        try:
            # Check if exists
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = ?", (cat,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Categories (category_name) VALUES (?)", (cat,))
                print(f" - Added: {cat}")
            else:
                print(f" - Exists: {cat}")
        except Exception as e:
            print(f" - Error adding {cat}: {e}")
    
    conn.commit()
    conn.close()
    print("Database update complete.")

if __name__ == "__main__":
    add_transfer_categories()
