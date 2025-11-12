from passlib.context import CryptContext # 비밀번호를 암호화 하여 저장하기 위해서 "passlib" 설치 필요 (pip install "passlib[bcrypt]")
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User


# 비밀번호는 탈취되더라도 복호화 할 수 없는 값으로 암호화 해서 저장해야 함
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto') 

def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username = user_create.username,
        password = pwd_context.hash(user_create.password1), # 암호화 된 비밀번호
        email = user_create.email
    )
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()