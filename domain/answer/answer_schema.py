import datetime

from pydantic import BaseModel, field_validator

from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str

    # content 값이 없거나 빈 값("")인 경우, 오류 발생하도록 설정
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None