# Encrypts a file using AESGCM encryption and then encrypts the AES key using RSA encryption via the provided public key file.

# Usage: python encryptor.py <input_file> <public_key_file>
# Output: the encrypted file which contains the nonce, the encrypted AES key, and the encrypted data. Concatenated in that specific order.


from sys import argv
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def get_public_key_from_file(public_key_file):
    # Get the RSA public key from the PEM file
    with open(public_key_file, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def encrypt_file_with_aes(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Generate a random AES key and nonce for encryption
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)  # AESGCM requires a 12-byte nonce

    # Encrypt the file data with AES
    encrypted_data = AESGCM(aes_key).encrypt(nonce, file_data, None)

    return aes_key, nonce, encrypted_data

def encrypt_aes_key_with_rsa(aes_key, public_key):
    # Encrypt the AES key using the RSA public key
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_aes_key

def export_encrypted_data_into_file(encrypted_data, nonce, encrypted_aes_key, output_file="encrypted_file"):
    with open(output_file, "wb") as f:
        f.write(nonce + encrypted_aes_key + encrypted_data)
    print(f"Encrypted data written to {output_file}")

if __name__ == "__main__":
    # Keeping it simple without extra handling!
    if len(argv) != 3:
        print("Usage: python encryptor.py <input_file> <public_key_file>")
        exit(1)
    input_file = argv[1]
    public_key_file = argv[2]

    public_key = get_public_key_from_file(public_key_file)
    
    aes_key, nonce, encrypted_data = encrypt_file_with_aes(input_file)
    encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, public_key)
    export_encrypted_data_into_file(encrypted_data, nonce, encrypted_aes_key)
    