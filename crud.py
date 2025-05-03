from sqlalchemy.orm import Session
from . import models, schemas

#criar usuário no banco de dados
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#obter usuário pelo seu nome de usuário
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

#buscar usuário por ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

#Listar usuários(com limite)
def get_all_users(db: Session, skip: int = 0, limit = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#atualizando email
def update_user_email(db: Session, user_id: int, new_email: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
    return user

#deletar usuário
def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
