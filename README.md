# AMD Takehome Project

Thank you for your patience.

This folder contains the following files and directories, sorted alphabetically:

- `AMD_image_file.JPG`
- `decrypted_image.JPG`
- `encrypted_file`
- `ex1/`
  - `generate_rsa_keys.py`
- `ex2/`
  - `hasher.py`
- `ex3/`
  - `decryptor.py`
  - `encryptor.py`
  - `test.py`
- `private_key.pem`
- `public_key.pem`
- `requirements.in`

## Exercise 1

### `ex1/generate_rsa_keys.py`
Generates an RSA key pair with a key size of 2048 bits.

Usage:
```bash
python generate_rsa_keys.py
```

Output:
- `private_key.pem`
- `public_key.pem`

Example outputs in this folder:
- `private_key.pem`
- `public_key.pem`

## Exercise 2

### `ex2/hasher.py`
Generates the SHA-256 hash of an input file and prints it in hexadecimal format to standard output.

Usage:
```bash
python hasher.py <input_file>
```

Output:
- SHA-256 hash of the input file in hex encoding

## Exercise 3

This exercise includes a two-part solution.

### `ex3/encryptor.py`
Encrypts a file using AES-GCM, then encrypts the AES key using RSA with the provided public key.

Usage:
```bash
python encryptor.py <input_file> <public_key_file>
```

Output:
- An encrypted file containing the nonce, the encrypted AES key, and the encrypted data in that exact order.

Example output in this folder:
- `encrypted_file`

### `ex3/decryptor.py`
Decrypts an encrypted JPG image produced by `encryptor.py` using the provided RSA private key.

Usage:
```bash
python decryptor.py <encrypted_file> <private_key_file>
```

Output:
- A decrypted JPG image

Example output in this folder:
- `decrypted_image.JPG`

### `ex3/test.py`
A sandbox file used for testing and developing the final solution implemented in `encryptor.py` and `decryptor.py`.

## Supporting Files

### `AMD_image_file.JPG`
The original image from the attached email, as-is.

### `requirements.in`
Contains the Python dependency needed to run the scripts:
- `cryptography`

### terminal_screenshot.png
A screenshot of these scripts in action on my terminal, with the expected outputs.
