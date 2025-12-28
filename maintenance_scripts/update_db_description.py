from db_connection import DBConnection
import pyodbc

def update_schema_description():
    conn = DBConnection.get_connection()
    if not conn:
        print("Connection failed.")
        return

    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT description FROM Transactions")
        print("Column 'description' already exists.")
    except:
        print("Column 'description' missing. Adding it...")
        try:
            # Add column description (nullable, default empty string)
            cursor.execute("ALTER TABLE Transactions ADD description NVARCHAR(255) DEFAULT ''")
            conn.commit()
            print("Column added.")
        except Exception as e:
            print(f"Error adding column: {e}")
            return
            
    conn.close()

if __name__ == "__main__":
    update_schema_description()
