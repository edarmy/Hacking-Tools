import quopri
import codecs

def encode_q(email, charset="iso-8859-1"):
    """
    Encodes an email address using the "encoded-word" Q encoding standard.
    """
    try:
        local_part, domain = email.split("@")
        # Q encoding: Convert each character to its hex representation
        encoded_local_part = ''.join(f"={ord(c):02X}" for c in local_part)
        return f"=?{charset}?q?{encoded_local_part}?=@{domain}"
    except Exception as e:
        return f"Error: {e}"

def encode_utf7(email):
    """
    Encodes an email address using UTF-7 encoding in the MIME encoded-word format.
    """
    try:
        local_part, domain = email.split("@")
        
        # Convert local-part to bytes using utf-8 encoding
        byte_local_part = local_part.encode('utf-8')
        
        # Encode the bytes in UTF-7
        encoded_local_part = codecs.encode(byte_local_part, "utf-7").decode('utf-7')
        
        # Replace UTF-7 specific characters
        encoded_local_part = encoded_local_part.replace("+", "&").rstrip("-")
        
        # Wrap in MIME encoded-word format
        return f"=?utf-7?q?{encoded_local_part}?=@{domain}"
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Email Encoding Program")
    print("Choose encoding type:")
    print("1. Q Encoding (Encoded-Word Standard)")
    print("2. UTF-7 Encoding (Encoded-Word Standard)")
    
    choice = input("Enter your choice (1/2): ").strip()
    email = input("Enter email to encode: ").strip()
    
    if choice == "1":
        charset = input("Enter charset for Q encoding (default: iso-8859-1): ").strip() or "iso-8859-1"
        encoded_email = encode_q(email, charset)
    elif choice == "2":
        encoded_email = encode_utf7(email)
    else:
        print("Invalid choice. Please select 1 or 2.")
        return
    
    print("\nEncoded email:")
    print(encoded_email)

if __name__ == "__main__":
    main()
