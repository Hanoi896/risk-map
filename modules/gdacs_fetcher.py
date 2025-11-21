# modules/gdacs_fetcher.py
import requests
import xmltodict
import json
import os
from datetime import datetime, timezone
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection # init_db는 여기서 호출 안 함
from app_config import GDACS_RSS_FEED # app_config.py 에서 RSS 피드 URL 가져오기
import sqlite3

GDACS_CATEGORY_MAP = {
    "EQ": "Earthquakes", "TC": "Tropical Cyclone", "FL": "Floods",
    "VO": "Volcanoes", "DR": "Drought", "WF": "Wildfires"
}
DEFAULT_GDACS_CATEGORY = "Disaster"

def parse_gdacs_date(date_str):
    if not date_str: return None
    formats_to_try = [
        "%Y-%m-%dT%H:%M:%SZ",      # '2024-07-22T06:42:00Z' (gdacs:fromdate)
        "%Y-%m-%dT%H:%M:%S.%fZ",   # 가끔 마이크로초 포함 Z
        "%a, %d %b %Y %H:%M:%S GMT", # 'Mon, 22 Jul 2024 06:55:02 GMT' (pubDate)
        "%a, %d %b %Y %H:%M:%S %Z",  # 일반적인 RFC1123 (시간대 정보 포함)
    ]
    dt_object = None
    for fmt in formats_to_try:
        try:
            # 'Z'를 fromisoformat이나 strptime이 직접 처리 못하는 경우가 있어, UTC로 가정하고 처리
            if fmt.endswith('Z') and date_str.endswith('Z'):
                 # datetime.fromisoformat은 Python 3.7+ 에서 Z를 잘 처리함
                if sys.version_info >= (3, 7):
                    dt_object = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else: # 구버전 호환용 (strptime은 Z 직접 처리 못함)
                    dt_object = datetime.strptime(date_str[:-1], fmt[:-1]).replace(tzinfo=timezone.utc)
            elif fmt == "%a, %d %b %Y %H:%M:%S GMT" and date_str.endswith(" GMT"):
                 dt_object = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc) # GMT는 UTC
            else:
                dt_object = datetime.strptime(date_str, fmt) # strptime은 naive datetime 반환 가능성

            if dt_object:
                # naive datetime이면 UTC로 가정
                if dt_object.tzinfo is None or dt_object.tzinfo.utcoffset(dt_object) is None:
                    dt_object = dt_object.replace(tzinfo=timezone.utc)
                # 모든 날짜를 UTC로 통일하여 ISO 형식으로 반환
                return dt_object.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        except ValueError:
            continue # 다음 형식 시도
    # print(f"경고: GDACS 날짜 파싱 실패 (모든 형식 시도): {date_str}")
    return None

def fetch_and_save_gdacs_data():
    print(f"GDACS 데이터 수집 시작: {GDACS_RSS_FEED}")
    try:
        response = requests.get(GDACS_RSS_FEED, timeout=30)
        response.raise_for_status()
        data_dict = xmltodict.parse(response.content.decode('utf-8', errors='replace'))
    except Exception as e:
        print(f"GDACS 데이터 가져오기 또는 파싱 실패: {e}")
        return

    processed_events_for_db = []
    items_in_feed = 0
    if 'rss' in data_dict and 'channel' in data_dict['rss'] and 'item' in data_dict['rss']['channel']:
        items = data_dict['rss']['channel']['item']
        if not isinstance(items, list): items = [items] if items else []
        items_in_feed = len(items)

        for item in items:
            try:
                event_type_code = item.get('gdacs:eventtype')
                event_id_val = item.get('gdacs:eventid', item.get('guid', {}).get('#text', str(datetime.now().timestamp()))) # ID 확보
                unique_id = f"gdacs-{event_id_val}-{event_type_code or 'unknown'}"

                category = GDACS_CATEGORY_MAP.get(event_type_code, event_type_code or DEFAULT_GDACS_CATEGORY)
                event_date_str = item.get('gdacs:fromdate') or item.get('pubDate') # todate보다 fromdate나 pubDate 선호
                parsed_date = parse_gdacs_date(event_date_str)
                if not parsed_date: continue

                point_str = item.get('georss:point')
                longitude, latitude = None, None
                if point_str:
                    try:
                        lat_str, lon_str = point_str.split()
                        latitude, longitude = float(lat_str), float(lon_str)
                    except ValueError: continue # 좌표 파싱 실패
                else: continue # 좌표 없으면 저장 안 함 (지도 표시 불가)

                description_text = item.get('description', '')
                if isinstance(description_text, dict) and '#cdata-section' in description_text:
                    description_text = description_text['#cdata-section']
                elif isinstance(description_text, dict):
                    description_text = str(description_text)
                
                event_data = {
                    "id": unique_id, "title": item.get('title', '제목 없음'),
                    "link": item.get('link'), "description": description_text,
                    "date": parsed_date, "category": category,
                    "original_category_code": event_type_code,
                    "alert_level": item.get('gdacs:alertlevel'),
                    "country": item.get('gdacs:country'),
                    "longitude": longitude, "latitude": latitude
                }
                processed_events_for_db.append(event_data)
            except Exception as e:
                print(f"GDACS 아이템 처리 중 오류: {item.get('title', '제목 없음')}. 오류: {e}")
                continue
    
    print(f"GDACS 피드에서 {items_in_feed}개 아이템 발견, {len(processed_events_for_db)}개 처리됨.")
    
    if not processed_events_for_db:
        print("DB에 저장할 GDACS 이벤트가 없습니다.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    saved_count = 0
    skipped_count = 0
    for event in processed_events_for_db:
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO gdacs_events 
            (id, title, link, description, date, category, original_category_code, alert_level, country, longitude, latitude) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event["id"], event["title"], event["link"], event["description"], event["date"],
                event["category"], event["original_category_code"], event["alert_level"],
                event["country"], event["longitude"], event["latitude"]
            ))
            saved_count += 1
        except sqlite3.Error as e:
            print(f"GDACS 이벤트 DB 저장 실패 (ID: {event['id']}): {e}")
            skipped_count +=1
            
    conn.commit()
    conn.close()
    print(f"GDACS 이벤트 {saved_count}개 DB 저장 완료. {skipped_count}개 건너<0xEB><0x9C><0x9C>.")

if __name__ == "__main__":
    from database import init_db
    init_db()
    fetch_and_save_gdacs_data()