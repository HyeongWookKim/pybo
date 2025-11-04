# import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./pybo.db' # 프로젝트 루트 디렉토리에 저장

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # SQLite는 "파일 기반 데이터베이스"라서, 기본적으로 하나의 스레드에서만 DB에 접근 가능하도록 막아둠
    # 이러한 제한을 해제해주는 옵션이 ```check_same_thread = False``` -> 즉, 여러 스레드에서 동시에 DB 접근이 가능하도록 설정
    connect_args = {'check_same_thread': False}
)
# autoflush: 쿼리를 실행하기 전에 변경된 내용을 DB 버퍼에 자동 반영할지 여부
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base() # 데이터베이스 모델 구성 시 사용

# DB session 관리해주는 제너레이터 생성
# @contextlib.contextmanager # 컨텍스트 매니저 객체를 반환 -> "with get_db() as db: ~~~" 사용 시에 적용
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()