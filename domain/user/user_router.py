from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer # pip install python-multipart, pip install "python-jose[cryptography]"
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 분 단위로 설정
SECRET_KEY = 'feacc99cae4cfa0f2fc1fcd694f665fda385c0f3816aba57b0db825f1f478a46' # 암호화 시 사용하는 64자리 랜덤 문자열 -> "openssl rand -hex 32" 명령어를 통해 얻을 수 있음
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/api/user/login')

router = APIRouter(
    prefix = '/api/user'
)

@router.post('/create', status_code = status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create = _user_create)
    if user: # user가 이미 존재하는 경우
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = '이미 존재하는 사용자입니다.')
    user_crud.create_user(db = db, user_create = _user_create)

@router.post('/login', response_model = user_schema.Token)
# username과 password의 값은 OAuth2PasswordRequestForm을 통해 얻어올 수 있음
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    # Make access token
    data = {
        'sub': user.username, # 사용자 명
        'exp': datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) # Token 유효기간
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.username
    }

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers = {'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM]) # 헤더 정보의 token 값을 읽어 사용자 객체를 리턴
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username = username)
        if user is None:
            raise credentials_exception
        return user