from cryptography.fernet import Fernet

secret_key = Fernet.generate_key()
print(secret_key.decode())
