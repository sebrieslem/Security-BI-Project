from cryptography.fernet import Fernet
import os

# === Standard File Names (Relative) ===
input_file = "tayara_vehicles_cleaned.csv"
encrypted_file = "tayara_vehicles_cleaned_encrypted.csv"
key_file = "encryption.key"

# === Step 1: Generate or Load Key ===
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    print("✅ Encryption key generated and saved as 'encryption.key'")
else:
    with open(key_file, "rb") as f:
        key = f.read()
    print("✅ Encryption key loaded from 'encryption.key'")

# === Step 2: Initialize Fernet ===
fernet = Fernet(key)

# === Step 3: Read and Encrypt the CSV ===
try:
    with open(input_file, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(encrypted_file, "wb") as f:
        f.write(encrypted)

    print(f"✅ File encrypted and saved as: {encrypted_file}")

except FileNotFoundError:
    print(f"❌ File not found: {input_file}")
except Exception as e:
    print(f"❌ Encryption failed: {e}")
