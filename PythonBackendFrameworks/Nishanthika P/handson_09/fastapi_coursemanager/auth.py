"""
auth.py
Hands-On 9, Task 1 & 2: registration, login, and the current-user
dependency used to protect routes.

OAuth2 Authorization Code flow vs this simple JWT login (Task 2, step 95):
The Authorization Code flow is designed for THIRD-PARTY clients acting on
a user's behalf without ever seeing their password: the user is redirected
to the auth server, logs in there, the auth server redirects back with a
short-lived "code", and the client exchanges that code (plus a client
secret) for an access token - usually also getting a refresh token so it
can renew access without the user logging in again. Our simple JWT login
above is the much lighter "Resource Owner Password" style: the client
collects the email/password directly and trades them for a token in one
call. That's fine for a first-party API + frontend you control, but you'd
never want a third-party app collecting your users' raw passwords, which
is exactly the problem the Authorization Code flow solves.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User as UserModel
from schemas import UserRegister, UserResponse, Token, LoginRequest
from security import get_password_hash, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')


@router.post('/register/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    """Task 1, step 88: register a new user; 409 if the email is taken."""
    existing = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail='Email is already registered')

    user = UserModel(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),  # never store the raw password
        is_active=1,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post('/login/', response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Task 2, step 91: verify credentials, issue a 30-minute JWT."""
    result = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect email or password')

    access_token = create_access_token(data={'sub': user.email})
    return Token(access_token=access_token)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """Task 2, step 92: decode + validate the JWT, return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get('sub')
    if email is None:
        raise credentials_exception

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
