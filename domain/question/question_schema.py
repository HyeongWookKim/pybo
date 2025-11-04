import datetime

from pydantic import BaseModel


# Question 스키마
class Question(BaseModel):
    # <참고>
    # Default 값이 없으면 필수 항목임을 의미함
    # 만약 필수 항목이 아니게 설정하려면 "subject: str | None = None"처럼 입력해주면 됨
    id: int
    subject: str
    content: str
    create_date: datetime.datetime