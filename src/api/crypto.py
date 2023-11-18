from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.constant_time import bytes_eq
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from hashlib import blake2b


def encrypt(key: bytes, nonce: bytes, data: bytes):
    return ChaCha20Poly1305(key=key).encrypt(
        associated_data=None, data=data, nonce=nonce
    )


def decrypt(key: bytes, nonce: bytes, data: bytes):
    return ChaCha20Poly1305(key=key).decrypt(
        associated_data=None, data=data, nonce=nonce
    )


def create_mac(key: bytes, data: bytes) -> bytes:
    assert len(key) == 32, f"Key must be length 32, it is currently {len(key)} long"
    mac = blake2b(data, digest_size=32, key=key).digest()
    return mac


def verify_mac(key: bytes, mac: bytes, data: bytes) -> tuple[bool, bytes]:
    assert len(key) == 32, f"Key must be length 32, it is currently {len(key)} long"
    assert len(mac) == 32, f"Mac must be length 32, it is currently {len(mac)} long"
    calculated_mac = blake2b(data, digest_size=32, key=key).digest()
    return bytes_eq(mac, calculated_mac), calculated_mac


def derive_key(
    password: bytes, salt: bytes, difficulty: int = 14, length: int = 64
) -> bytes:
    return Scrypt(
        salt=salt,
        length=length,
        n=2 ** difficulty,
        r=8,
        p=1,
    ).derive(password)
