from src.api import utils
from src.api import crypto
from os import urandom


# | Offset | Size | Encrypted | Description                 |
# | ------ | ---- | --------- | --------------------------- |
# | 0      | 32   | No        | Volume digest using blake2b |
# | 32     | 32   | No        | KDF Salt                    |
# | 64     | 32   | No        | Cipher Salt                 |
# | 96     | 8    | Yes       | String "EV_FILE$"           |
# | 104    | 1024 | Yes       | Reserved                    |
# | 1128   | Var. | Yes       | Files                       |


def create_volume(filename: str, password: bytes):
    volume: bytearray = bytearray(1128)  # Set first 1160 bytes to 00
    kdf_salt: bytes = urandom(32)
    cipher_salt: bytes = urandom(32)

    key = crypto.derive_key(
        password=password, salt=kdf_salt
    )  # First half is for encryption, second is for the MAC

    volume[32:64] = kdf_salt
    volume[64:96] = cipher_salt
    volume[96:104] = b"EV_FILE$"

    volume[0:32] = crypto.create_mac(key=key[32:64], data=volume[32:])

    encrypted_volume = volume[0:96] + bytearray(
        crypto.encrypt(key=key[0:32], data=volume[96:], nonce=b"\x00" * 12)
    )

    utils.write(f"volumes\\{filename}.ev", encrypted_volume)


def decrypt_volume(filename: str, password: bytes):
    encrypted_volume = utils.read(f"volumes\\{filename}.ev")

    mac = encrypted_volume[0:32]
    kdf_salt = encrypted_volume[32:64]
    cipher_salt = encrypted_volume[64:96]
    key = crypto.derive_key(
        password=password, salt=kdf_salt
    )  # First half is for encryption, second is for the MAC

    decrypted_data = crypto.decrypt(
        key=key[0:32], data=encrypted_volume[96:], nonce=b"\x00" * 12
    )

    assert crypto.verify_mac(
        key=key[32:64], mac=mac, data=encrypted_volume[32:96] + decrypted_data
    ), "Invalid MAC"

    return decrypted_data
