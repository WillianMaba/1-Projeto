from pydantic import BaseModel, EmailStr

#criação de usuário (entrada)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

#retorno(saída)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class config:
        orm_mode = True