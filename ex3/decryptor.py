# Decrypts an encrypted .JPG image output from encryptor.py using the provided RSA private key file.
# The input encrypted_file, being the product of encryptor.py, contains the nonce, the encrypted AES key, and the encrypted data concatenated in that specific order.

# Usage: python decryptor.py <encrypted_file> <private_key_file>
# Output: decrypted .JPG image


from sys import argv
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes

def unpack_encrypted_file(encrypted_file):
    with open(encrypted_file, "rb") as f:
        file_content = f.read()

    nonce_length = 12  # AESGCM requires a 12-byte nonce
    aes_key_length = 256  # RSA key size is 2048 bits, or 256 bytes

    # The first 12 bytes are the nonce
    nonce = file_content[:nonce_length]

    # The next 256 bytes are the encrypted AES key
    encrypted_aes_key = file_content[nonce_length:nonce_length + aes_key_length]

    # The rest is the encrypted data
    encrypted_data = file_content[nonce_length + aes_key_length:]

    return nonce, encrypted_aes_key, encrypted_data

def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key_file):
    # Get the RSA private key from the PEM file
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Decrypt the AES key using the RSA private key
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key

def decrypt_image(encrypted_data, nonce, aes_key):
    # Decrypt the image data
    aesgcm = AESGCM(aes_key)
    decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)

    return decrypted_data

def export_decrypted_image(decrypted_data, output_file="decrypted_image.JPG"):
    with open(output_file, "wb") as f:
        f.write(decrypted_data)
    print(f"Decrypted image written to {output_file}")

if __name__ == "__main__":
    # Keeping it simple without extra handling!
    if len(argv) != 3:
        print("Usage: python decryptor.py <encrypted_file> <private_key_file>")
        exit(1)
    encrypted_file = argv[1]
    private_key_file = argv[2]

    nonce, encrypted_aes_key, encrypted_data = unpack_encrypted_file(encrypted_file)
    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key_file)
    decrypted_data = decrypt_image(encrypted_data, nonce, aes_key)

    export_decrypted_image(decrypted_data)