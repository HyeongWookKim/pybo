from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
# from models import Question


router = APIRouter(
    prefix = '/api/question'
)

# response_model = list[question_schema.Question] -> question_list 함수의 return 값은 Question 스키마로 구성된 리스트임을 의미
@router.get('/list', response_model = list[question_schema.Question]) # URL = '/api/question/list'
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)

    ### FastAPI의 Depends를 사용하지 않을 경우, 아래처럼 with 문을 사용하면 됨 ###
    # with get_db() as db:
    #     _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

    return _question_list

@router.get('/detail/{question_id}', response_model = question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id = question_id)
    return question