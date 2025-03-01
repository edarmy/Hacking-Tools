#!/bin/bash

# Function to encode using Q encoding (MIME)
encode_q() {
    local email="$1"
    local charset="$2"
    
    # Split the email into local-part and domain
    local local_part=$(echo "$email" | cut -d'@' -f1)
    local domain=$(echo "$email" | cut -d'@' -f2)
    
    # Encode local-part using Q encoding (hex representation)
    local encoded_local_part=""
    for ((i=0; i<${#local_part}; i++)); do
        local c="${local_part:i:1}"
        encoded_local_part+="=$(printf '%02X' "'$c")"
    done
    
    # Return the final encoded email
    echo "=?$charset?q?$encoded_local_part?=@$domain"
}

# Function to encode using UTF-7 encoding (MIME)
encode_utf7() {
    local email="$1"
    
    # Split the email into local-part and domain
    local local_part=$(echo "$email" | cut -d'@' -f1)
    local domain=$(echo "$email" | cut -d'@' -f2)

    # Encode the local-part using UTF-7 encoding
    # First, we use the iconv to convert to UTF-7
    local encoded_local_part=$(echo "$local_part" | iconv -f utf-8 -t utf-7)

    # Replace UTF-7 specific characters with MIME-safe alternatives
    encoded_local_part=$(echo "$encoded_local_part" | sed 's/+/&/g' | sed 's/-$//')

    # Return the final encoded email
    echo "=?utf-7?q?$encoded_local_part?=@$domain"
}

# Main function to prompt user for input
main() {
    echo "Email Encoding Program"
    echo "Choose encoding type:"
    echo "1. Q Encoding (Encoded-Word Standard)"
    echo "2. UTF-7 Encoding (Encoded-Word Standard)"
    
    read -p "Enter your choice (1/2): " choice
    read -p "Enter email to encode: " email
    
    if [ "$choice" == "1" ]; then
        read -p "Enter charset for Q encoding (default: iso-8859-1): " charset
        charset=${charset:-iso-8859-1}
        encoded_email=$(encode_q "$email" "$charset")
    elif [ "$choice" == "2" ]; then
        encoded_email=$(encode_utf7 "$email")
    else
        echo "Invalid choice. Please select 1 or 2."
        return
    fi
    
    echo -e "\nEncoded email:"
    echo "$encoded_email"
}

# Call the main function
main
