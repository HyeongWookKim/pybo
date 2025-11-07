from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
# from models import Question
from starlette import status


router = APIRouter(
    prefix = '/api/question'
)

# response_model = list[question_schema.Question] -> question_list 함수의 return 값은 Question 스키마로 구성된 리스트임을 의미
@router.get('/list', response_model = question_schema.QuestionList) # URL = '/api/question/list'
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(db, skip = page * size, limit = size)
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get('/detail/{question_id}', response_model = question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id = question_id)
    return question

@router.post('/create', status_code = status.HTTP_204_NO_CONTENT) # Return 할 값이 없으므로 204(응답 없음) return 
def question_create(_question_create: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    question_crud.create_question(db = db, question_create = _question_create)