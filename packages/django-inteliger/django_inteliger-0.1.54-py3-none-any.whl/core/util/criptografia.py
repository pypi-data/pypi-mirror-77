import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 1_217


def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    """
    :Nome da classe/função: Email
    :descrição: Função para criptografar senha
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    :param message: mensagem a ser criptografada
    :param password: senha usada para criptografar
    :param iterations: numero de iteracoes para criptografar
    :return: Senha criptografada
    """
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    """
    :Nome da classe/função: Email
    :descrição: Função para descriptografar senha
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    :param token: Token criptografado
    :param password: Senha usada para criptografrar
    :return: senha descriptografada
    """
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)