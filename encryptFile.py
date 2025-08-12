from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import json

# Load public key
with open("C:/SSM LAB/SSMPROJECT/shared/public.pem", "rb") as f:
    pub_key = RSA.import_key(f.read())

# File to encrypt
with open("C:/SSM LAB/SSMPROJECT/Sender_admin/qp.pdf", "rb") as f:
    plaintext = f.read()

# AES encryption
aes_key = get_random_bytes(32)
iv = get_random_bytes(16)
cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
ciphertext = cipher_aes.encrypt(pad(plaintext, AES.block_size))

# Encrypt AES key with RSA
cipher_rsa = PKCS1_OAEP.new(pub_key)
enc_aes_key = cipher_rsa.encrypt(aes_key)

# Save encrypted components
data = {
    "enc_key": enc_aes_key.hex(),
    "iv": iv.hex(),
    "ciphertext": ciphertext.hex(),
    "exam_time": "2025-04-08 20:30:00"  # in UTC
}

with open("C:/SSM LAB/SSMPROJECT/shared/encrypted_exam.json", "w") as f:
    json.dump(data, f)

print("Encrypted file saved to shared/encrypted_exam.json.")
