"""
Symmetric encryption and decryption using AES-256 in CBC mode.
Run this file directly to print out a new randomly generated key.
"""

import sys, os
import argparse
import base64
import secrets
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


def generate_key():
    """Generate a random 32-byte key for AES-256"""
    key = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(key).decode("utf-8")


def encrypt(data: bytes, key_str: str) -> bytes:
    # Decode the base64 key
    key = base64.urlsafe_b64decode(key_str)

    # Generate a random IV
    iv = secrets.token_bytes(16)

    # Pad the data to be a multiple of block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Create HMAC for authentication
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(iv + ciphertext)
    hmac_digest = h.finalize()

    # Combine IV, ciphertext, and HMAC
    return iv + ciphertext + hmac_digest


def encrypt_file(file: str, outfile: str, key: str):
    with open(file, "rb") as f:
        data = f.read()
    encrypted = encrypt(data, key)
    with open(f"{outfile}", "wb") as f:
        f.write(encrypted)


def decrypt(data: bytes, key_str: str) -> bytes:
    # Decode the base64 key
    key = base64.urlsafe_b64decode(key_str)

    # Extract IV, ciphertext, and HMAC
    iv = data[:16]
    hmac_digest = data[-32:]  # SHA256 produces 32 bytes
    ciphertext = data[16:-32]

    # Verify HMAC
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(iv + ciphertext)
    try:
        h.verify(hmac_digest)
    except Exception:
        raise ValueError("HMAC verification failed: Data may have been tampered with")

    # Decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


def decrypt_file(file: str, outfile: str, key: str):
    with open(file, "rb") as f:
        data = f.read()
    decrypted = decrypt(data, key)
    with open(f"{outfile}", "wb") as f:
        f.write(decrypted)


# Run as script. With no parameters, will generate a new key. Use -key to specify key to use,
# and -encrypt  or -decrypt  to encrypt / decrypt a file to disk
# Use -out  to specify output filename, otherwise will default to .enc or .dec
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encrypt and decrypt files. Uses AES-256 in CBC mode with HMAC-SHA256 authentication. Run without arguments to generate a new key."
    )
    parser.add_argument("file", nargs="?", help="File to encrypt/decrypt")
    parser.add_argument(
        "-k",
        "--key",
        help="Encryption key to use. If not provided, a new one will be generated",
    )
    parser.add_argument(
        "-d",
        "--decrypt",
        action="store_true",
        help="Decrypt file instead of encrypting",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="Output filename. Defaults to input filename with .enc or .dec extension",
    )
    args = parser.parse_args()

    # Use provided key or generate new one
    if args.key:
        key = args.key
        print("Using provided key")
    else:
        key = generate_key()
        print(f"New key: {key}")
        if not args.file:
            sys.exit()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    # Handle encryption
    if not args.decrypt:
        out = args.out if args.out else args.file + ".enc"
        encrypt_file(args.file, out, key)
        print(f"Encrypted {args.file} -> {out}")

    # Handle decryption
    else:
        if args.out:
            out = args.out
        elif args.file.endswith(".enc"):
            # Remove .enc extension if present
            out = args.file[:-4]
        else:
            out = args.file + ".dec"

        decrypt_file(args.file, out, key)
        print(f"Decrypted {args.file} -> {out}")
