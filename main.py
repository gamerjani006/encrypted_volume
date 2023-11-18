from src.api import crypto
from src.api import volume


def main():
    # volume.create_volume("myvolume", b"password123")
    print(
        volume.decrypt_volume("myvolume", b"password123")
    )


if __name__ == '__main__':
    main()
