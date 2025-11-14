from pydantic import BaseModel, field_validator, EmailStr # email_validator 설치 필요 (pip install "pydantic[email]")
from pydantic_core.core_schema import FieldValidationInfo


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr # EmailStr은 해당 값이 이메일 형식과 일치하는지 검증하기 위해 사용 (이메일 형식과 일치하지 않을 경우 오류가 발생)

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        # info.data에는 UserCreate의 속성들이 {변수명: 값, ...} 형태로 전달
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v
    
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class User(BaseModel):
    id: int
    username: str
    email: str