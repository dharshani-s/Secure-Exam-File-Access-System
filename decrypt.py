
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
import json, datetime 
from zoneinfo import ZoneInfo  # zoneinfo - module, ZoneInfo - class for a specific time zone
import pyotp

''' datetime.datetime: for creating/handling date-time objects

    datetime.timezone.utc: for setting/using UTC timezone

    datetime.timedelta: for doing date/time arithmetic
'''

# Load private RSA key
with open("C:/SSM LAB/SSMproject/Receiver_faculty/private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# Load TOTP secret key
with open("totp_secret.txt", "r") as f:
    totp_secret = f.read().strip()

# OTP verification using Google Authenticator
totp = pyotp.TOTP(totp_secret)
MAX_ATTEMPTS = 3
for attempt in range(MAX_ATTEMPTS):
    otp = input("Enter OTP from Google Authenticator: ")
    if totp.verify(otp):
        print("OTP verified successfully.")
        break
    else:
        print("Invalid OTP.")
else:
    print("Too many failed attempts. Exiting.")
    exit()

# Load encrypted exam data
with open("C:/SSM LAB/SSMPROJECT/shared/encrypted_exam.json", "r") as f:
    data = json.load(f) #dictionay, json's key val format

# Parse exam time (assumed to be in UTC in JSON)
 #from datetime import datetime
# its datetime.datetime since 1st is a module second is a class inside it
exam_time_utc = datetime.datetime.strptime(data["exam_time"], "%Y-%m-%d %H:%M:%S")
exam_time_utc = exam_time_utc.replace(tzinfo=datetime.timezone.utc)

# Get current time in UTC from system and takes timezone as laptop's time zone setting
now_utc = datetime.datetime.now(datetime.timezone.utc)

# Check if access is within the allowed window
if now_utc < (exam_time_utc - datetime.timedelta(hours=2)):
    print("Access denied. You can only decrypt this file 2 hours before the exam.")
    print(f"Exam starts at: {exam_time_utc.astimezone(ZoneInfo('Asia/Kolkata'))}") #astimezone(ZoneInfo()) - convert one timezone to another, an instance method part of datetime module
    print(f"Current time: {now_utc.astimezone(ZoneInfo('Asia/Kolkata'))}") #for smtg else : Asia/Dubai (+4 hrs)
    exit()

# Decrypt AES key using RSA
enc_key = bytes.fromhex(data["enc_key"]) #data is a created dictionary so its accessible this way
iv = bytes.fromhex(data["iv"])
ciphertext = bytes.fromhex(data["ciphertext"])

cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(enc_key)

# Decrypt exam file
cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

# Save decrypted PDF
with open("C:/SSM LAB/SSMproject/Receiver_faculty/decrypted_exam.pdf", "wb") as f:
    f.write(decrypted)

print("Decryption successful. Saved as 'decrypted_exam.pdf'")
