# Application to generate SHA-256 hash of the attached file. No signing is needed. Just print hash in HEX encoding to standard output.

# Usage: python hasher.py <input_file>
# Output: SHA-256 hash of the input file in HEX encoding


from sys import argv
from cryptography.hazmat.primitives import hashes

def generate_sha256_hash_from_bytes(file_bytes):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file_bytes)
    hash_bytes = digest.finalize()
    return hash_bytes.hex()

def generate_sha256_hash_from_file(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()
    sha256_hash = generate_sha256_hash_from_bytes(file_data)
    print(f"SHA-256 Hash in HEX: {sha256_hash}")

if __name__ == "__main__":
    # Keeping it simple without extra handling!
    if len(argv) != 2:
        print("Usage: python hasher.py <input_file>")
        exit(1)
    
    generate_sha256_hash_from_file(argv[1])