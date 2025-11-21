# database.py
import sqlite3
import os

DATABASE_DIR = "data"
DATABASE_NAME = "disaster_data.db"
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

def get_db_connection():
    """데이터베이스 연결 객체를 반환합니다."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # 컬럼 이름으로 접근 가능하도록 설정
    return conn

def init_db():
    """데이터베이스 테이블을 초기화합니다."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # EONET 이벤트 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eonet_events (
        id TEXT PRIMARY KEY,
        title TEXT,
        category TEXT,
        date TEXT, -- ISO 8601 format
        score INTEGER,
        longitude REAL,
        latitude REAL,
        raw_geometry TEXT -- 원본 geometry JSON 문자열 (필요시)
    )
    ''')

    # GDACS 이벤트 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gdacs_events (
        id TEXT PRIMARY KEY,
        title TEXT,
        link TEXT,
        description TEXT,
        date TEXT, -- ISO 8601 format
        category TEXT,
        original_category_code TEXT,
        alert_level TEXT,
        country TEXT,
        longitude REAL,
        latitude REAL,
        source TEXT DEFAULT 'GDACS'
    )
    ''')

    # Disease 이벤트 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disease_events (
        id TEXT PRIMARY KEY,
        title TEXT,
        link TEXT,
        date TEXT, -- ISO 8601 format
        category TEXT DEFAULT 'Disease Outbreak',
        description TEXT,
        country TEXT,
        country_iso3 TEXT,
        longitude REAL, -- 좌표 정보가 있을 경우
        latitude REAL,  -- 좌표 정보가 있을 경우
        source_data TEXT
    )
    ''')
    
    # 인덱스 추가 (쿼리 성능 향상)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_eonet_date_category ON eonet_events (date, category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_gdacs_date_category ON gdacs_events (date, category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_disease_date_country ON disease_events (date, country)")


    conn.commit()
    conn.close()
    print("데이터베이스 초기화 완료 (테이블 생성됨).")

if __name__ == '__main__':
    # 이 스크립트를 직접 실행하면 DB와 테이블이 생성됩니다.
    init_db()