from user_controller import UserController
from transaction_controller import TransactionController
import datetime

def verify_transfer():
    print("--- Verifying Transfer Feature (Enhanced) ---")
    
    # 1. Setup Dummy Users
    user1 = "UserA_" + datetime.datetime.now().strftime("%H%M%S")
    user2 = "UserB_" + datetime.datetime.now().strftime("%H%M%S")
    
    UserController.register_user(user1, "pass")
    UserController.register_user(user2, "pass")
    
    id1 = UserController.get_user_id_by_username(user1)
    id2 = UserController.get_user_id_by_username(user2)
    print(f"User IDs: {user1}={id1}, {user2}={id2}")

    # 2. Add initial funds to User1
    # Check what categories valid
    cats = TransactionController.get_categories()
    if not cats:
        print("Error: No categories found!")
        return
    
    salary_cat = next((c['id'] for c in cats if 'Salary' in c['name']), cats[0]['id'])
    print(f"Using Category ID {salary_cat} for Income")

    res, msg = TransactionController.add_transaction(id1, salary_cat, 1000.0, "Income", "2025-01-01")
    print(f"Add Funds Result: {res}, {msg}")
    
    bal1 = TransactionController.get_balance(id1)
    print(f"Bal1 after add: {bal1}")

    # 3. Perform Transfer
    transfer_amount = 200.0
    res, msg = TransactionController.process_transfer(id1, id2, transfer_amount, "2025-01-02")
    print(f"Transfer Result: {res}, {msg}")

    # 4. Check Final
    bal1_final = TransactionController.get_balance(id1)
    bal2_final = TransactionController.get_balance(id2)
    print(f"Final Bal1: {bal1_final}")
    print(f"Final Bal2: {bal2_final}")

    # Inspect History for User 2
    print("User 2 History:")
    rows = TransactionController.get_user_transactions(id2)
    for r in rows:
         print(r)

if __name__ == "__main__":
    verify_transfer()
