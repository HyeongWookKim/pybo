from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router
from domain.answer import answer_router


app = FastAPI()

# CORS 예외 주소 등록
origins = [
    'http://localhost:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

# app 객체에 router 객체 등록 (Router 객체를 생성해서 FastAPI app에 등록해야만 라우팅 기능이 동작함)
app.include_router(question_router.router)
app.include_router(answer_router.router)