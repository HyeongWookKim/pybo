from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


# 질문 추천을 위해 사용할 테이블 객체 -> ManyToMany(N:M) 관계
question_voter = Table(
    'question_voter', # 테이블 명
    Base.metadata, 
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key = True)
)

# Answer 모델에 voter 속성 추가
answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key = True)
)

class Question(Base):
    __tablename__ = 'question' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True) # 질문 데이터의 고유 번호 (PK -> 자동 생성됨)
    subject = Column(String, nullable = False) # 질문 제목
    content = Column(Text, nullable = False) # 질문 내용
    create_date = Column(DateTime, nullable = False) # 질문 작성일시
    user_id = Column(Integer, ForeignKey('user.id'), nullable = True)
    user = relationship('User', backref = 'question_users') # 유저 모델에서 질문 모델을 참조하기 위함 / backref: 역참조 설정 (즉, 유저에서 질문을 거꾸로 참조)
    modify_date = Column(DateTime, nullable = True) # 수정일시는 수정이 발생한 경우에만 생성되므로 null 허용
    voter = relationship('User', secondary = question_voter, backref = 'question_voters') # <주의> 동일한 모델로 relationship 속성을 생성할 때, backref 이름은 중복될 수 없음
    # voter의 relationship 함수에서 secondary 값으로 위에서 생성한 question_voter 테이블 객체를 지정
    # 이렇게 하면 Question 모델을 통해 추천인을 저장하면, 실제 데이터는 question_voter 테이블에 저장되고, 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조 가능


class Answer(Base):
    __tablename__ = 'answer' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True) # 답변 데이터의 고유 번호 (PK -> 자동 생성됨)
    content = Column(Text, nullable = False) # 답변 내용
    create_date = Column(DateTime, nullable = False) # 답변 작성일시
    question_id = Column(Integer, ForeignKey('question.id', ondelete = 'CASCADE')) # question 테이블의 id 컬럼 참조 (FK) / "CASCADE": 부모가 삭제되면 자식도 같이 삭제됨
    question = relationship('Question', backref = 'answers') # 답변 모델에서 질문 모델을 참조하기 위함 / backref: 역참조 설정 (즉, 질문에서 답변을 거꾸로 참조)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = True)
    user = relationship('User', backref = 'answer_users') # 유저 모델에서 답변 모델을 참조하기 위함 / backref: 역참조 설정 (즉, 유저에서 답변을 거꾸로 참조)
    modify_date = Column(DateTime, nullable = True) # 수정일시는 수정이 발생한 경우에만 생성되므로 null 허용
    voter = relationship('User', secondary = answer_voter, backref = 'answer_voters') # <주의> 동일한 모델로 relationship 속성을 생성할 때, backref 이름은 중복될 수 없음


class User(Base):
    __tablename__ = 'user' # 모델에 의해 관리되는 테이블 명

    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False) # 중복 허용 X
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False) # 중복 허용 X