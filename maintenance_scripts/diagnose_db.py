import pyodbc
import sys

def diagnose():
    print("--- Database Connection Diagnostic ---")
    
    # 1. Check Drivers
    drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    print(f"Detected SQL Server Drivers: {drivers}")
    if not drivers:
        print("ERROR: No SQL Server ODBC drivers found!")
        print("Solution: Install ODBC Driver 17 for SQL Server.")
        return

    driver = drivers[0]
    print(f"Using Driver: {driver}")

    # 2. Check Server Names
    # Common local server names
    servers = ['localhost', '.', '(local)', r'.\SQLEXPRESS', r'localhost\SQLEXPRESS']
    # Attempt to read computer name from environment? 
    # For now let's stick to these common ones.
    
    database = 'SmartPayDB'
    
    success_config = None

    for server in servers:
        print(f"\nTesting connection to Server: '{server}' ...")
        conn_str = (
            f'DRIVER={{{driver}}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'Trusted_Connection=yes;'
        )
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            print("  [SUCCESS] Connected!")
            conn.close()
            success_config = server
            break
        except Exception as e:
            print(f"  [FAILED] {str(e)}")

    if success_config:
        print(f"\n>>> DIAGNOSIS COMPLETE: The correct server name is '{success_config}'.")
        print(f">>> Please update 'db_connection.py' to use server = '{success_config}'")
    else:
        print("\n>>> DIAGNOSIS FAILED: Could not connect to any common server name.")
        print("Possible causes:")
        print("1. SQL Server is not running.")
        print("2. The database 'SmartPayDB' does not exist (Did you run the setup script?).")
        print("3. You are using a named instance not in the list (e.g., COMPUTERNAME\INSTANCE).")
        print("4. Your SQL Server requires username/password authentication.")

if __name__ == "__main__":
    diagnose()
