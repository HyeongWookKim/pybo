# import contextlib

from sqlalchemy import create_engine, MetaData # SQLite 데이터베이스에서 사용하는 인덱스 등의 제약 조건 이름은 MetaData 클래스를 사용하여 규칙을 정의
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
# 데이터베이스의 Primary Key, Unique Key, Index Key 등의 이름 규칙을 새롭게 정의
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}
Base.metadata = MetaData(naming_convention = naming_convention)

# DB session 관리해주는 제너레이터 생성
# @contextlib.contextmanager # 컨텍스트 매니저 객체를 반환 -> "with get_db() as db: ~~~" 사용 시에 적용
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()