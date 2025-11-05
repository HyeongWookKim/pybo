import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer


# Question 스키마
class Question(BaseModel):
    # <참고>
    # Default 값이 없으면 필수 항목임을 의미함
    # 만약 필수 항목이 아니게 설정하려면 "subject: str | None = None"처럼 입력해주면 됨
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = [] # 모델에서 backref = 'answers'라고 설정해줬기 때문에, 반드시 answers라는 이름을 사용해야 함

class QuestionCreate(BaseModel):
    subject: str
    content: str

    # subject, content 값이 없거나 빈 값("")인 경우, 오류 발생하도록 설정
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v