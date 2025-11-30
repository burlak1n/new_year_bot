import base64

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from app.config import encryption_key


def encrypt_data(data: str) -> str:
    chacha = ChaCha20Poly1305(encryption_key)
    nonce = b"\x00" * 12
    encrypted = chacha.encrypt(nonce, data.encode(), None)
    return base64.urlsafe_b64encode(encrypted).decode().rstrip("=")


def decrypt_data(encrypted_data: str) -> str:
    chacha = ChaCha20Poly1305(encryption_key)
    nonce = b"\x00" * 12
    padded = encrypted_data + "=" * (4 - len(encrypted_data) % 4)
    encrypted_bytes = base64.urlsafe_b64decode(padded)
    decrypted = chacha.decrypt(nonce, encrypted_bytes, None)
    return decrypted.decode()
