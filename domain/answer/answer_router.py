from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud


router = APIRouter(
    prefix = '/api/answer'
)

@router.post('/create/{question_id}', status_code = status.HTTP_204_NO_CONTENT) # Return 할 값이 없으므로 204(응답 없음) return 
def answer_create(question_id: int, 
                  _answer_create: answer_schema.AnswerCreate, 
                  db: Session = Depends(get_db)):
    
    # Create answer
    question = question_crud.get_question(db, question_id = question_id)
    if not question: # 질문이 없는 경우, 에러 발생하도록 설정
        raise HTTPException(status_code = 404, detail = 'Question not found')
    answer_crud.create_answer(db, question = question, answer_create = _answer_create)