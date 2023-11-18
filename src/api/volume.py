from src.api import utils
from src.api import crypto
from os import urandom


def create_volume(filename: str, password: bytes):
    # | Offset | Size | Encrypted | Description                 |
    # | ------ | ---- | --------- | --------------------------- |
    # | 0      | 32   | No        | Volume digest using blake2b |
    # | 32     | 32   | No        | KDF Salt                    |
    # | 64     | 32   | No        | Cipher Salt                 |
    # | 96     | 8    | Yes       | String "EV_FILE$"           |
    # | 104    | 1024 | Yes       | Reserved                    |
    # | 1128   | Var. | Yes       | Files                       |

    volume: bytearray = bytearray(1128)  # Set first 1160 bytes to 00
    kdf_salt: bytes = urandom(32)
    cipher_salt: bytes = urandom(32)

    key = crypto.derive_key(password=password, salt=kdf_salt)  # First half is for encryption, second is for the MAC

    volume[32:64] = kdf_salt
    volume[64:96] = cipher_salt
    volume[96:104] = b"EV_FILE$"

    volume[0:32] = crypto.create_mac(
        key=key[32:64],
        data=volume[32:]
    )

    encrypted_volume = volume[0:96] + bytearray(
        crypto.encrypt(
            key=key[0:32],
            data=volume[96:],
            nonce=b"\x00" * 12
        )
    )

    utils.write(f"volumes\\{filename}.ev", encrypted_volume)
