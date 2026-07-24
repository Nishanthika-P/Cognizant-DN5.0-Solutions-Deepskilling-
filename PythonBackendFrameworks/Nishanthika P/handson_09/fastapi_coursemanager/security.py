"""
security.py
Hands-On 9, Task 1, step 87: password hashing utilities.

bcrypt vs MD5/SHA-256 (step 89):
MD5 and SHA-256 are designed to be FAST - great for checksums, terrible
for passwords, because an attacker with a leaked hash database can try
billions of guesses per second on commodity hardware (or GPUs).
bcrypt (and similarly scrypt/argon2) is deliberately SLOW and has a
tunable "work factor" - each guess costs meaningfully more compute time,
which makes large-scale brute-force / dictionary attacks impractical
even if the hash database leaks. bcrypt also auto-salts every hash,
so identical passwords never produce identical hashes.
"""
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# In a real app these come from environment variables / a secrets manager -
# never hard-code a production secret key.
SECRET_KEY = 'dev-only-secret-change-me'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Hands-On 9, Task 2, step 91: JWT with a 30-minute expiry by default."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
