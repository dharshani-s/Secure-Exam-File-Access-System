import pyotp
import qrcode

# Generate base32 secret for TOTP
secret = pyotp.random_base32()
print("Your TOTP Secret (keep it safe):", secret)

# Generate TOTP URI and QR code
uri = pyotp.totp.TOTP(secret).provisioning_uri(
    name="faculty@university.edu", issuer_name="ExamSecure"
)

# Save the QR code as an image
qrcode.make(uri).save("totp_qr.png")
print("Scan the QR code in 'totp_qr.png' with Google Authenticator.")

# Save secret for later use
with open("totp_secret.txt", "w") as f:
    f.write(secret)
