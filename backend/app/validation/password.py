from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano en su hash Argon2,
    listo para guardarse en Usuario.password_hash.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si una contraseña en texto plano coincide con un hash
    ya almacenado, sin necesidad de revertir el hash (imposible por diseño).
    """
    return password_hash.verify(plain_password, hashed_password)