from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User
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
def question_create(_question_create: question_schema.QuestionCreate, 
                    db: Session = Depends(get_db), 
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db = db, question_create = _question_create, user = current_user)

@router.put('/update', status_code = status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_update.question_id)
    if not db_question: # 조회 결과(데이터)가 없는 경우
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '데이터를 찾을 수 없습니다.')
    if current_user.id != db_question.user.id: # 질문 작성자와 현재 로그인 한 사용자가 동일하지 않은 경우
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '수정 권한이 없습니다.')
    question_crud.update_question(db = db, db_question = db_question, question_update = _question_update)

@router.delete('/delete', status_code = status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete, 
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_delete.question_id)
    if not db_question: # 조회 결과(데이터)가 없는 경우
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '데이터를 찾을 수 없습니다.')
    if current_user.id != db_question.user.id: # 질문 작성자와 현재 로그인 한 사용자가 동일하지 않은 경우
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '삭제 권한이 없습니다.')
    question_crud.delete_question(db = db, db_question = db_question)

@router.post('/vote', status_code = status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id = _question_vote.question_id)
    if not db_question: # 답변 데이터가 없는 경우
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '데이터를 찾을 수 없습니다.')
    question_crud.vote_question(db, db_question = db_question, db_user = current_user) # 질문에 추천인 등록