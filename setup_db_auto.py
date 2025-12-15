import pyodbc
import re

def run_setup():
    server = r'localhost\SQLEXPRESS'
    driver_name = 'ODBC Driver 17 for SQL Server'
    
    # Check if driver exists
    drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    if drivers:
        driver_name = drivers[0]
    
    print(f"Connecting to 'master' on {server} using {driver_name}...")
    
    conn_str = (
        f'DRIVER={{{driver_name}}};'
        f'SERVER={server};'
        f'DATABASE=master;'
        f'Trusted_Connection=yes;'
        f'AutoCommit=True;'
    )
    
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
    except Exception as e:
        print(f"Failed to connect to master: {e}")
        return

    print("Connected to master. Reading SQL script...")
    
    with open('database_setup.sql', 'r') as f:
        sql_script = f.read()

    # Split by 'GO' (case insensitive)
    commands = re.split(r'\bGO\b', sql_script, flags=re.IGNORECASE)

    cursor = conn.cursor()
    
    for cmd in commands:
        if cmd.strip():
            try:
                # Remove 'USE SmartPayDB' if we are creating it, 
                # but actually pyodbc might not handle USE if we are in master?
                # The script has 'USE master; GO; ... CREATE DATABASE ... USE SmartPayDB ...'
                # We should execute them. 
                # However, if we are in master, and we execute 'USE SmartPayDB', checks might fail if not committed.
                # But autocommit is True.
                print(f"Executing: {cmd[:50].strip()}...")
                cursor.execute(cmd)
            except Exception as e:
                # Ignore "database already exists" error if it happens
                if "already exists" in str(e):
                    print("  -> Database/Table already exists.")
                else:
                    print(f"  -> Error: {e}")

    conn.close()
    print("Database setup completed.")

if __name__ == "__main__":
    run_setup()
