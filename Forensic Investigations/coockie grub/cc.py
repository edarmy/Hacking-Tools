import os
import sqlite3
import shutil
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import win32crypt  # Only needed for Windows systems
import base64
import json
import time

def copy_cookies_db(cookie_db_path):
    """
    Attempts to copy the Chrome cookies database to a temporary location.
    If the file is locked, it will retry a few times before giving up.
    """
    temp_db_path = 'temp_cookies.db'
    retries = 5
    for _ in range(retries):
        try:
            shutil.copy2(cookie_db_path, temp_db_path)
            return temp_db_path
        except PermissionError:
            print("File is locked. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
    print("Failed to copy the cookies database after several retries.")
    return None

def get_all_chrome_profiles():
    """
    Retrieves all Chrome profiles from the 'User Data' folder.

    Returns:
        List[str]: A list of profile names.
    """
    user_data_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    if not os.path.exists(user_data_path):
        print(f"Chrome user data path not found at {user_data_path}")
        return []

    profiles = [f.name for f in Path(user_data_path).iterdir() if f.is_dir() and f.name.startswith('Profile')]
    profiles.append('Default')  # Add the default profile as well

    return profiles

def get_chrome_cookies(profile='Default'):
    """
    Extracts cookies from Google Chrome's local database.

    Args:
        profile (str): The Chrome profile to extract cookies from (default is 'Default').

    Returns:
        List[dict]: A list of cookies, where each cookie is a dictionary.
    """
    user_data_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', profile)
    cookie_db_path = os.path.join(user_data_path, 'Network', 'Cookies')

    if not os.path.exists(cookie_db_path):
        print(f"Cookie database not found at {cookie_db_path}")
        return []

    temp_db_path = copy_cookies_db(cookie_db_path)
    if not temp_db_path:
        return []

    cookies = []

    try:
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT host_key, name, path, encrypted_value FROM cookies")

        for host_key, name, path, encrypted_value in cursor.fetchall():
            decrypted_value = decrypt_cookie(encrypted_value)
            cookies.append({
                'host': host_key,
                'name': name,
                'path': path,
                'value': decrypted_value,
            })

    except Exception as e:
        print(f"Error extracting cookies from {profile}: {e}")

    finally:
        conn.close()
        os.remove(temp_db_path)

    return cookies

def decrypt_cookie(encrypted_value):
    """
    Decrypts an encrypted cookie value using Windows DPAPI.

    Args:
        encrypted_value (bytes): The encrypted cookie value.

    Returns:
        str: The decrypted cookie value.
    """
    try:
        if encrypted_value[:3] == b'v10':
            key = get_encryption_key()
            nonce = encrypted_value[3:15]
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(nonce),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            return decryptor.update(encrypted_value[15:]) + decryptor.finalize()
        else:
            return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
    except Exception as e:
        print(f"Failed to decrypt cookie: {e}")
        return ''

def get_encryption_key():
    """
    Retrieves the AES encryption key for Chrome's cookies.

    Returns:
        bytes: The AES encryption key.
    """
    key_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')

    with open(key_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)

    encrypted_key = local_state['os_crypt']['encrypted_key']
    decrypted_key = win32crypt.CryptUnprotectData(base64.b64decode(encrypted_key)[5:], None, None, None, 0)[1]

    return decrypted_key

if __name__ == "__main__":
    profiles = get_all_chrome_profiles()

    for profile in profiles:
        print(f"Extracting cookies from profile: {profile}")
        cookies = get_chrome_cookies(profile)
        for cookie in cookies:
            print(cookie)
