from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Question(Base):
    __tablename__ = 'question' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True) # 질문 데이터의 고유 번호 (PK -> 자동 생성됨)
    subject = Column(String, nullable = False) # 질문 제목
    content = Column(Text, nullable = False) # 질문 내용
    create_date = Column(DateTime, nullable = False) # 질문 작성일시


class Answer(Base):
    __tablename__ = 'answer' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True) # 답변 데이터의 고유 번호 (PK -> 자동 생성됨)
    content = Column(Text, nullable = False) # 답변 내용
    create_date = Column(DateTime, nullable = False) # 답변 작성일시
    question_id = Column(Integer, ForeignKey('question.id', ondelete = 'CASCADE')) # question 테이블의 id 컬럼 참조 (FK) / "CASCADE": 부모가 삭제되면 자식도 같이 삭제됨
    question = relationship('Question', backref = 'answers') # 답변 모델에서 질문 모델을 참조하기 위함 / backref: 역참조 설정 (즉, 질문에서 답변을 거꾸로 참조)


class User(Base):
    __tablename__ = 'user' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False) # 중복 허용 X
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False) # 중복 허용 X