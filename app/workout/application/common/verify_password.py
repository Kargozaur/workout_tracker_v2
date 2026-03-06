import re


def verify_password(value: str) -> str:
    """Verifies that the given password is correct based on regex.
    Password must have at least 1 upper case symbol, 1 special symbol,
    1 number and be at least 8 characters long.
    """
    if not re.search(r"[A-Z]", value):
        raise ValueError("password.uppercase_required")
    if not re.search(r"\d", value):
        raise ValueError("password.number_required")
    if not re.search(r"[!@#$%^&*(),.:<>|?]", value):
        raise ValueError("password.specialsymbol_required")
    if len(value) < 8:
        raise ValueError("password.length_8_symbols_required")
    return value
