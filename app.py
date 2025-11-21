# app.py
from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json # jsonify를 위해 여전히 필요
from datetime import datetime # timedelta는 여기서는 직접 사용 안 함

# database.py 에서 get_db_connection 임포트
# 프로젝트 루트에 database.py가 있다고 가정
from database import get_db_connection, DATABASE_PATH # DATABASE_PATH도 임포트하여 파일 존재 확인

# modules에서 weather_fetcher 임포트
from modules.weather_fetcher import get_weather_by_coords

app = Flask(__name__)

def events_to_dict_list(events_from_db):
    """DB에서 가져온 Row 객체 리스트를 딕셔너리 리스트로 변환합니다."""
    if events_from_db is None:
        return []
    return [dict(row) for row in events_from_db]

@app.route('/')
def index():
    current_year = datetime.now().year
    # index.html 템플릿에 현재 연도 전달
    return render_template('index.html', current_year=current_year)

@app.route("/api/eonet")
def get_eonet_events():
    conn = None # finally 블록에서 사용하기 위해 미리 선언
    try:
        conn = get_db_connection()
        year_filter = request.args.get('year')
        category_filter = request.args.get('category')

        # 기본 쿼리: 필요한 컬럼만 선택
        query = "SELECT id, title, category, date, score, longitude, latitude FROM eonet_events"
        conditions = []
        params = []

        if year_filter:
            conditions.append("strftime('%Y', date) = ?")
            params.append(year_filter)
        if category_filter:
            conditions.append("category = ?")
            params.append(category_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # 최근 데이터 우선 정렬 및 결과 수 제한 (성능 고려)
        query += " ORDER BY date DESC LIMIT 1000" 

        events_cursor = conn.execute(query, params)
        events = events_cursor.fetchall()
        
        return jsonify(events_to_dict_list(events))
    except Exception as e:
        print(f"EONET DB 쿼리 오류: {e}")
        return jsonify({"error": "EONET 데이터 조회 중 서버 오류 발생"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/gdacs")
def get_gdacs_events():
    conn = None
    try:
        conn = get_db_connection()
        # GDACS도 필터링 추가 가능 (예: alert_level, country 등)
        # 여기서는 모든 GDACS 이벤트의 최근 500개만 가져옴
        query = "SELECT id, title, link, description, date, category, original_category_code, alert_level, country, longitude, latitude, source FROM gdacs_events ORDER BY date DESC LIMIT 500"
        events_cursor = conn.execute(query)
        events = events_cursor.fetchall()
        return jsonify(events_to_dict_list(events))
    except Exception as e:
        print(f"GDACS DB 쿼리 오류: {e}")
        return jsonify({"error": "GDACS 데이터 조회 중 서버 오류 발생"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/disease")
def get_disease_events():
    conn = None
    try:
        conn = get_db_connection()
        # 질병 데이터도 필터링 추가 가능 (예: country)
        country_filter = request.args.get('country') # 예시: ?country=Korea
        
        query = "SELECT id, title, link, date, category, description, country, country_iso3, longitude, latitude, source_data FROM disease_events"
        conditions = []
        params = []

        if country_filter:
            # 국가명(영문) 또는 ISO3 코드로 검색 (LIKE 사용)
            conditions.append("(country LIKE ? OR country_iso3 LIKE ?)")
            params.extend([f"%{country_filter}%", f"%{country_filter}%"]) # 부분 일치 검색
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY date DESC LIMIT 500" # 최근 500개
        
        events_cursor = conn.execute(query, params)
        events = events_cursor.fetchall()
        return jsonify(events_to_dict_list(events))
    except Exception as e:
        print(f"질병 정보 DB 쿼리 오류: {e}")
        return jsonify({"error": "질병 정보 데이터 조회 중 서버 오류 발생"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/api/weather")
def get_weather():
    try:
        lat = request.args.get("lat", type=float)
        lon = request.args.get("lon", type=float)
    except ValueError:
        return jsonify({"error": "잘못된 위도 또는 경도 형식입니다."}), 400

    if lat is None or lon is None:
        return jsonify({"error": "위도와 경도는 필수 항목입니다."}), 400

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return jsonify({"error": "유효하지 않은 위도 또는 경도 범위입니다."}), 400
        
    weather_data = get_weather_by_coords(lat, lon)
    
    if "error" in weather_data: # weather_fetcher에서 오류 발생 시
        return jsonify(weather_data), 500 # 또는 적절한 상태 코드
        
    return jsonify(weather_data)

# Flask 앱이 static 파일을 직접 제공하도록 설정
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == "__main__":
    # 앱 시작 시 DB 파일 존재 여부 확인
    # DATABASE_PATH는 database.py에서 가져온 변수 사용
    if not os.path.exists(DATABASE_PATH):
        print(f"경고: 데이터베이스 파일({DATABASE_PATH})이 없습니다.")
        print("애플리케이션이 정상적으로 동작하지 않을 수 있습니다.")
        print("1. `python database.py`를 실행하여 데이터베이스와 테이블을 초기화하세요.")
        print("2. 각 fetcher 스크립트 (예: `python modules/eonet_fetcher.py`)를 실행하여 데이터를 채우세요.")
    else:
        print(f"데이터베이스 파일({DATABASE_PATH}) 확인됨.")
    
    # host='0.0.0.0'으로 설정하여 외부에서도 접근 가능하도록 할 수 있음 (개발 시 주의)
    app.run(debug=True, host='0.0.0.0', port=5000)