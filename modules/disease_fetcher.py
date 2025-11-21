# modules/disease_fetcher.py
import requests
import json
import os
from datetime import datetime, timezone, timedelta
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection # init_db는 여기서 호출 안 함
import sqlite3

RELIEFWEB_API_URL = "https://api.reliefweb.int/v1/reports"

def fetch_and_save_disease_data(days_to_fetch=90): # 최근 90일 데이터 기본
    print(f"질병 발생 데이터 수집 시작 (ReliefWeb API - 최근 {days_to_fetch}일)...")
    
    payload = {
        "appname": "disaster-map-project-ko-db",
        "preset": "latest", "profile": "full", "limit": 100, # 한 번에 100개 요청
        "query": {"value": "disease OR epidemic OR outbreak OR pandemic", "operator": "OR"},
        "filter": {
            "operator": "AND",
            "conditions": [
                {"field": "format.name", "value": "Situation Report"},
                {
                    "field": "date.created",
                    "value": {
                        "from": (datetime.now(timezone.utc) - timedelta(days=days_to_fetch)).isoformat(timespec='seconds'),
                        "to": datetime.now(timezone.utc).isoformat(timespec='seconds')
                    }
                }
            ]
        }
    }

    try:
        # print(f"ReliefWeb API 요청 페이로드: {json.dumps(payload, indent=2)}") # 디버깅용
        response = requests.post(RELIEFWEB_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"질병 데이터 가져오기 또는 파싱 실패: {e}")
        if hasattr(e, 'response') and e.response is not None: # HTTPError의 경우
            try: print(f"API 에러 상세: {e.response.json()}")
            except: print(f"API 에러 응답 (텍스트): {e.response.text}")
        return

    processed_events_for_db = []
    items_in_response = 0
    if raw_data and "data" in raw_data:
        items_in_response = raw_data.get('count', len(raw_data['data']))
        for item_raw in raw_data.get("data", []):
            try:
                fields = item_raw.get("fields", {})
                title = fields.get("title", "제목 없음")
                date_created_str = fields.get("date", {}).get("created")
                if not date_created_str: continue

                try:
                    dt_object = datetime.fromisoformat(date_created_str.replace("Z", "+00:00"))
                    event_date = dt_object.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
                except ValueError: continue # 날짜 파싱 실패

                primary_country_obj = fields.get("primary_country")
                country_name, country_iso3, lon, lat = "알 수 없음", None, None, None
                if isinstance(primary_country_obj, list) and primary_country_obj: primary_country_obj = primary_country_obj[0]
                
                if isinstance(primary_country_obj, dict):
                    country_name = primary_country_obj.get("name", "알 수 없음")
                    country_iso3 = primary_country_obj.get("iso3")
                    loc = primary_country_obj.get("location")
                    if loc and isinstance(loc, dict): lon, lat = loc.get("lon"), loc.get("lat")

                # 좌표가 있는 경우에만 DB에 저장 (지도 표시 위함)
                if lon is None or lat is None:
                    # print(f"좌표 없는 질병 보고서 건너<0xEB><0x9C><0x9C>: {title}")
                    continue

                body = fields.get("body-html", fields.get("body", ""))
                desc = body[:500] + "..." if body else "내용 없음"
                event_id = f"disease-rw-{item_raw.get('id', date_created_str.replace(':','-').replace('+','-'))}"

                event_data = {
                    "id": event_id, "title": title, "link": fields.get("url_alias", fields.get("url")),
                    "date": event_date, "description": desc, "country": country_name, "country_iso3": country_iso3,
                    "longitude": float(lon) if lon is not None else None, # float으로 변환
                    "latitude": float(lat) if lat is not None else None,   # float으로 변환
                    "source_data": "ReliefWeb"
                }
                processed_events_for_db.append(event_data)
            except Exception as e:
                print(f"질병 아이템 처리 중 오류: {fields.get('title', '제목 없음')}. 오류: {e}")
                continue

    print(f"ReliefWeb API에서 {items_in_response}개 항목 수신, {len(processed_events_for_db)}개 처리됨 (좌표 있는 것만).")

    if not processed_events_for_db:
        print("DB에 저장할 질병 발생 이벤트가 없습니다.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    saved_count = 0
    skipped_count = 0
    for event in processed_events_for_db:
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO disease_events 
            (id, title, link, date, description, country, country_iso3, longitude, latitude, source_data) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event["id"], event["title"], event["link"], event["date"], event["description"],
                event["country"], event["country_iso3"], event["longitude"], event["latitude"],
                event["source_data"]
            ))
            saved_count += 1
        except sqlite3.Error as e:
            print(f"질병 이벤트 DB 저장 실패 (ID: {event['id']}): {e}")
            skipped_count += 1
            
    conn.commit()
    conn.close()
    print(f"질병 발생 이벤트 {saved_count}개 DB 저장 완료. {skipped_count}개 건너<0xEB><0x9C><0x9C>.")

if __name__ == "__main__":
    from database import init_db
    init_db()
    fetch_and_save_disease_data(days_to_fetch=3650) # 최근 90일 데이터 수집