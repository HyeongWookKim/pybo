from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# FileResponse, StaticFiles: 프론트엔드 빌드를 통해 생성한 파일을 FastAPI 서버가 서비스 할 수 있도록 해주기 위함
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router


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
app.include_router(user_router.router)
app.mount('/assets', StaticFiles(directory = 'frontend/dist/assets')) # 경로 매핑

@app.get('/')
def index(): # '/' 경로로 접속하면, "frontend/dist/index.html" 파일을 읽어서 서비스 할 수 있도록 index 함수 추가
    return FileResponse('frontend/dist/index.html') # FileResponse: FastAPI가 정적인 파일을 출력할 때 사용