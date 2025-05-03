from future.utils.surrogateescape import encoded
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional


#configuração para criptografar senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#configuração do jwt

SECRET_KEY = "05b73a763ce4449dda5fb0950e1218fd18a788105bb6c8aa35"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

#criptografando a senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#verificando se a senha corresponde ao hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#criando o token JWT
def create_acess_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verificando token jwt
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None



