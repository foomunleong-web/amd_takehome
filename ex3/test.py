# Application that will encrypt and decrypt the file using the RSA key pair generated

# The catch: RSA cannot encrypt data larger than the key size.
# The image is 74KB, way larger than 2048 bits or 256 bytes.
# We will need to encrypt the image using a simple encryption, such as symmetric encryption AES, 
# then encrypt the AES key using RSA.

from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pathlib import Path
import os

image_name = "AMD_image_file.JPG"
image_path = "{}/{}".format(Path(__file__).parent, image_name)

def generate_rsa_key_pair():
    # Generate a private key.
    private_key = rsa.generate_private_key(key_size=2048, public_exponent=65537)

    # Generate the corresponding public key
    public_key = private_key.public_key()

    return private_key, public_key

def generate_sha256_hash_from_bytes(file_bytes):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file_bytes)
    hash_bytes = digest.finalize()
    return hash_bytes.hex()

def encrypt_file_with_aes(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Get the SHA256 hash of the original file to validate at the end
    original_hash = generate_sha256_hash_from_bytes(file_data)

    # Generate a random AES key and nonce for encryption
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)  # AESGCM requires a 12-byte nonce

    # Encrypt the file data with AES
    encrypted_data = AESGCM(aes_key).encrypt(nonce, file_data, None)

    return original_hash, aes_key, nonce, encrypted_data

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

def decrypt_image(encrypted_data, nonce, encrypted_aes_key, private_key):
    # Obtain AES key
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the image data
    aesgcm = AESGCM(aes_key)
    decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)

    return decrypted_data


if __name__ == "__main__":
    private_key, public_key = generate_rsa_key_pair()
    original_hash, aes_key, nonce, encrypted_data = encrypt_file_with_aes(image_path)
    encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, public_key)
    decrypted_data = decrypt_image(encrypted_data, nonce, encrypted_aes_key, private_key)
    decrypted_hash = generate_sha256_hash_from_bytes(decrypted_data)

    assert original_hash == decrypted_hash, "Hashes do not match! Decryption failed."
    print("Hashes match. Decryption successful wow!")