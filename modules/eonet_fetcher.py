# modules/eonet_fetcher.py
import requests
import json
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection, init_db # init_db는 여기서 직접 호출 안해도 됨 (main에서 하거나, database.py 실행)
from scorer import score_event
import sqlite3 # sqlite3.Error 를 위해 임포트

def fetch_eonet_data_for_year(year):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    url = f"https://eonet.gsfc.nasa.gov/api/v3/events?start={start_date}&end={end_date}&status=all"
    print(f"EONET 데이터 수집 중 (연도: {year}): {url}")
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()
        print(f"EONET 데이터 수집 성공 (연도: {year}). 이벤트 {len(data.get('events', []))}개.")
        return data.get("events", [])
    except requests.Timeout:
        print(f"EONET 데이터 요청 시간 초과 (연도: {year}): {url}")
        return []
    except requests.RequestException as e:
        print(f"EONET 데이터 요청 실패 (연도: {year}): {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"EONET 데이터 JSON 디코딩 실패 (연도: {year}): {e} - 응답: {response.text[:200]}...")
        return []

def save_eonet_events_to_db(events_to_save):
    if not events_to_save:
        print("DB에 저장할 EONET 이벤트가 없습니다.")
        return 0, 0

    conn = get_db_connection()
    cursor = conn.cursor()
    saved_count = 0
    skipped_count = 0

    for event in events_to_save:
        longitude, latitude = None, None
        raw_geometry_str = None
        if event.get("geometry") and event["geometry"].get("coordinates"):
            coords = event["geometry"]["coordinates"]
            # EONET 좌표는 [longitude, latitude] 또는 [[[lon, lat], ...]] (Polygon) 등 다양
            # 여기서는 Point만 단순 처리. 나머지는 raw_geometry에 저장.
            if event["geometry"]["type"] == "Point" and len(coords) == 2 and \
               isinstance(coords[0], (int, float)) and isinstance(coords[1], (int, float)):
                longitude, latitude = coords[0], coords[1]
            raw_geometry_str = json.dumps(event["geometry"]) # 전체 geometry 저장

        try:
            cursor.execute('''
            INSERT OR REPLACE INTO eonet_events 
            (id, title, category, date, score, longitude, latitude, raw_geometry) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event["id"], event["title"], event["category"], event["date"], event["score"],
                longitude, latitude, raw_geometry_str
            ))
            saved_count += 1
        except sqlite3.Error as e:
            print(f"EONET 이벤트 DB 저장 실패 (ID: {event['id']}): {e}")
            skipped_count += 1
            
    conn.commit()
    conn.close()
    print(f"EONET 이벤트 {saved_count}개 DB 저장 완료. {skipped_count}개 건너<0xEB><0x9C><0x9C>.")
    return saved_count, skipped_count

def process_eonet_event_item(event_raw):
    """단일 EONET 원본 이벤트를 처리하여 저장할 형식으로 변환합니다."""
    if not all(k in event_raw for k in ("id", "title", "categories", "geometry")) or \
       not event_raw["categories"] or not event_raw["geometry"]:
        return None

    category_info_list = event_raw["categories"]
    event_date_to_use = None
    primary_geometry = None

    if event_raw.get("geometry") and isinstance(event_raw["geometry"], list) and len(event_raw["geometry"]) > 0:
        valid_geometries_with_dates = []
        for geom in event_raw["geometry"]:
            if "date" in geom and "coordinates" in geom:
                valid_geometries_with_dates.append(geom)
        
        if valid_geometries_with_dates:
            valid_geometries_with_dates.sort(key=lambda g: g["date"], reverse=True)
            primary_geometry = valid_geometries_with_dates[0]
            event_date_to_use = primary_geometry["date"]

    if not event_date_to_use:
        if event_raw.get("closed"): # 이벤트 종료 날짜
            event_date_to_use = event_raw.get("closed")
        elif primary_geometry and "date" in primary_geometry: # 위에서 못찾았지만 primary_geometry에 date가 있다면
             event_date_to_use = primary_geometry["date"]
        else: # 그래도 날짜 없으면 포기
            # print(f"날짜 정보 없는 EONET 이벤트 건너<0xEB><0x9C><0x9C>: ID {event_raw.get('id')}")
            return None
    
    if not primary_geometry: # geometry가 필수라고 가정
        # print(f"Geometry 정보 없는 EONET 이벤트 건너<0xEB><0x9C><0x9C>: ID {event_raw.get('id')}")
        return None
            
    event_for_scoring = {
        "category": category_info_list[0].get("title", "Unknown Category"),
        "date": event_date_to_use 
    }
    calculated_score = score_event(event_for_scoring)

    return {
        "id": event_raw["id"],
        "title": event_raw["title"],
        "category": category_info_list[0].get("title", "Unknown Category"),
        "geometry": primary_geometry,
        "date": event_date_to_use, 
        "score": calculated_score
    }

def fetch_and_process_eonet_historical_data(start_year=1960):
    current_year = datetime.now().year
    all_processed_events_for_db = []
    total_raw_events_count = 0

    print(f"EONET 역사 데이터 수집 및 처리 시작: {start_year}년부터 {current_year}년까지")

    for year in range(start_year, current_year + 1):
        yearly_events_raw = fetch_eonet_data_for_year(year)
        total_raw_events_count += len(yearly_events_raw)
        
        processed_this_year = []
        for event_raw_item in yearly_events_raw:
            processed_event = process_eonet_event_item(event_raw_item)
            if processed_event:
                processed_this_year.append(processed_event)
        
        all_processed_events_for_db.extend(processed_this_year)
        print(f"{year}년 데이터 처리 완료. {len(processed_this_year)}개 이벤트 준비됨. (누적 처리: {len(all_processed_events_for_db)})")
        # import time
        # time.sleep(0.2) # API 요청 간격

    print(f"총 {total_raw_events_count}개 원본 EONET 이벤트 수집. 중복 제거 및 DB 저장 시작...")
    
    unique_events_for_db = []
    seen_ids = set()
    for event in all_processed_events_for_db:
        if event["id"] not in seen_ids:
            unique_events_for_db.append(event)
            seen_ids.add(event["id"])
            
    print(f"중복 제거 후 총 {len(unique_events_for_db)}개의 EONET 이벤트 DB 저장 준비 완료.")
    save_eonet_events_to_db(unique_events_for_db)

if __name__ == "__main__":
    # 스크립트 실행 시 DB 테이블 확인 및 생성 (database.py의 init_db 호출)
    # 이 부분은 database.py를 직접 실행하거나, app.py 시작 시 한 번만 수행하는 것이 더 좋을 수 있음
    # 여기서는 fetcher 실행 시에도 테이블이 확실히 있도록 호출
    from database import init_db 
    init_db()

    # 1960년부터 현재까지 데이터 수집 실행 (매우 오래 걸릴 수 있음)
    # fetch_and_process_eonet_historical_data(start_year=1960)
    
    # 테스트를 위해 최근 1년치만 가져오기
    current_year = datetime.now().year
    # 1960년부터 현재까지 데이터 수집 실행
    fetch_and_process_eonet_historical_data(start_year=3650) # <--- 이 부분 확인!
