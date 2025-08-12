# Secure-Exam-File-Access-System
A high-security file access system for academic exams with:
- AES-CBC encryption + RSA (PKCS1_OAEP) for key protection
- Multi-factor authentication (TOTP + password)
- Timezone-aware restricted decryption window
- Password-protected PDF generation

- **EXECUTION FLOW:**
1. **Faculty** runs `generatekeys.py` → creates `public.pem` & `private.pem`.
2. **Admin** runs `totp_setup.py` → generates `totp_qr.png` & `totp_secret.txt` (faculty scans QR code in Google Authenticator upon sharing as a protected pdf)
3. **Admin** runs `encrypt.py` → encrypts `questionpaper.pdf` with `public.pem` & MFA lock → creates `encrypted_exam.json`.
4. Admin shares `/shared` folder with faculty.
5. **Faculty** runs `decrypt.py` → enters TOTP (from authenticator) & password → retrieves `decrypted_exam.pdf`.

  FILE HIERARCHY OF THE PROJECT:
  ```
SecureExamFileAccessSystem/
│
├── sender_admin/
│   ├── encrypt.py
│   ├── questionpaper.pdf
│   ├── totp_setup.py
│
├── receiver_faculty/
│   ├── decrypt.py
│   ├── generatekeys.py
│   ├── private.pem
│   ├── decrypted_exam.pdf   
│
├── shared/
│   ├── encrypted_exam.json
│   ├── public.pem
│
├── totp_qr.png
├── totp_qr-protected
├── totp_secret.txt ```
