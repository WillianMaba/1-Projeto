from os import access
from fastapi import FastAPI, Depends, HTTPException, status,  Path, Body
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from database import SessionLocal, engine
from datetime import timedelta

#criando tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#obtendo sessão no banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#registrar um novo usuário
@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user:schemas.UserCreate, db: Session = Depends(get_db())):
#verificar se o usuário ja existe
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already registered")

#criptografar a senha
    hashed_password = auth.hash_password(user.password)

#criando um novo usuário no bd
    new_user = crud.create_user(db, user, hashed_password)

    return new_user

#login de usuário(gerando token)

@app.post("/login/")
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username = user.username)


#verificar usuário existente e senha corretamente
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")

    # listar usuários
@app.get("/users/", response_model=list[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(auth.verify_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return crud.get_all_users(db, skip= skip, limit= limit)

#buscar usuário por ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int= Path(...), db: Session = Depends(get_db), token: str = Depends(auth.verify_token())):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

#Atualizando email
@app.put("/users/{user_id}/email", response_model=schemas.UserResponse)
def update_email(user_id: int, new_email: str = Body(...), db: Session= Depends(get_db), token: str = Depends(auth.verify_token())):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    update_user = crud.update_user_email(db, user_id, new_email)
    if not update_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return update_user

#deletando usuário
@app.delete("/users{user_id}", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db),token: str = Depends(auth.verify_token())):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid Token")

    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return deleted_user


#gerando o token JWT
    access_token = auth.create_acess_token(data={"sub": db_user.username})

    return {"acess_token": access_token, "tocken_type": "bearer"}

#rota com acesso apenas com token válido
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(auth.verify_token())):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

#Recupera usuário com base no seu nome de usuário.
    db_user = crud.get_user_by_username(db, username=token["sub"])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    return db_user
