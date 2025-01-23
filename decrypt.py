import base64
import os
from Crypto.Cipher import AES

def decrypt_file(encrypted_file_path, decryption_key, output_file_path):
    # Convert the decryption key to bytes
    key = decryption_key.encode('utf-8')

    # Read the encrypted file
    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = base64.b64decode(file.read())

    # Extract the IV and the actual encrypted data
    iv = encrypted_data[:16]  # First 16 bytes are the IV for AES-CBC
    encrypted_bytes = encrypted_data[16:]

    # Initialize the AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_bytes)

    # Remove padding (PKCS7)
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    # Write the decrypted data to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decrypted_data)

    print(f"Decrypted file saved to: {output_file_path}")

if __name__ == "__main__":
    # Directory paths
    encrypted_dir = "exfil"
    decrypted_dir = "decrypt"

    # Create the "decrypt" directory if it doesn't exist
    os.makedirs(decrypted_dir, exist_ok=True)

    # Decryption key (must match the encryption key used)
    decryption_key = "0123456789abcdef0123456789abcdef"

    # Check if the "exfil" directory exists
    if not os.path.exists(encrypted_dir):
        print(f"Error: Encrypted directory '{encrypted_dir}' does not exist.")
        exit(1)

    # Process all files in the "exfil" directory
    for filename in os.listdir(encrypted_dir):
        encrypted_file_path = os.path.join(encrypted_dir, filename)
        output_file_path = os.path.join(decrypted_dir, filename)

        try:
            decrypt_file(encrypted_file_path, decryption_key, output_file_path)
        except Exception as e:
            print(f"Failed to decrypt {filename}: {e}")
