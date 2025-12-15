# Final Setup Checklist

The **Smart Pay App** is fully coded. Here is exactly what needs to be done to run it:

### 1. Install New Dependencies
The new features (QR Codes, PDF Receipts) require two libraries. Run this command:
```bash
python -m pip install qrcode[pil] fpdf
```

### 2. Verify Database
I have already updated your database, but if you reset it or move to another machine, run:
```bash
python update_db_account.py
```

### 3. Run the Application
Launch the main interface:
```bash
python main.py
```

### 4. Test New Features
- **Dashboard**: Check if your QR Code is visible.
- **Send Money**: Try sending money and click "Yes" to download the receipt.
- **History**: Select a row and click "Download Receipt".
