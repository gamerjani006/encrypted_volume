def write(path: str, data: bytes) -> True:
    with open(path, "wb") as f:
        f.write(data)
    return True


def convert_to_bytes(unit: str, amount: int):
    unit_table = {
        "byte": 1,
        "kilobyte": 1024,
        "megabyte": 1048576,
        "gigabyte": 1073741824,
    }
    assert unit in unit_table.keys() and amount > 0, f"Invalid unit {unit} or invalid amount {amount}"

    return unit_table.get(unit) * amount
