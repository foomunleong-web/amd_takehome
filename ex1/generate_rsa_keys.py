# Application to generate an RSA key pair, key size = 2048 bits

# Usage: python generate_rsa_keys.py
# Output: private_key.pem and public_key.pem files in the current directory


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_key_pair():
    # Generate a private key.
    # 65537 is the standard and most widely used public exponent in the RSA cryptosystem, it is also a prime number.
    # A different value is only useful for a specific compatibility requirement
    private_key = rsa.generate_private_key(key_size=2048, public_exponent=65537)

    # Generate the corresponding public key
    public_key = private_key.public_key()

    return private_key, public_key

# Export the RSA keys to PEM files.
# PEM is a base64 encoded format with header and footer lines.
def export_keys_to_files(private_key, public_key, private_key_file="private_key.pem", public_key_file="public_key.pem"):
    # Export the private key to a PEM file
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_key_file, "wb") as f:
        f.write(private_pem)
    print(f"Private key written to {private_key_file}")

    # Export the public key to a PEM file
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_file, "wb") as f:
        f.write(public_pem)
    print(f"Public key written to {public_key_file}")

if __name__ == "__main__":
    private_key, public_key = generate_rsa_key_pair()
    export_keys_to_files(private_key, public_key)