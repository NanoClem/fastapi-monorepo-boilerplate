import secrets
import string


def generate_prefixed_id(prefix: str) -> str:
    """Generates a web-safe, unique string ID.
    Example output: usr_2j8Fk9sA7bDx4mZ1pQ3wE

    Args:
        prefix (str): The prefix to prepend to the generated ID.

    Returns:
        str: A unique string ID with the specified prefix.
    """
    alphabet = string.ascii_letters + string.digits
    random_segment = "".join(secrets.choice(alphabet) for _ in range(21))
    return f"{prefix}_{random_segment}"
