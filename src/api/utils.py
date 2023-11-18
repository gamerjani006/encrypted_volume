def write(path: str, data: bytes) -> True:
    with open(path, "wb") as f:
        f.write(data)
    return True


def read(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def convert_to_bytes(unit: str, amount: int):
    unit_table = {
        "byte": 1,
        "kilobyte": 1024,
        "megabyte": 1048576,
        "gigabyte": 1073741824,
    }
    assert (
        unit in unit_table.keys() and amount > 0
    ), f"Invalid unit {unit} or invalid amount {amount}"

    return unit_table.get(unit) * amount
