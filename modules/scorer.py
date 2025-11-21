# modules/scorer.py
from datetime import datetime, timezone, timedelta

# 카테고리별 기본 가중치
# 이 값들은 이벤트의 초기 심각도를 나타냅니다.
# 점수 범위: 일반적으로 0-100점 사이로 조정하는 것이 일반적입니다.
# 여기서는 최대 110점 (90 + 20)까지 나올 수 있습니다. 필요시 정규화(normalize) 고려.
CATEGORY_WEIGHTS = {
    "Earthquakes": 90,
    "Volcanoes": 80,
    "Wildfires": 70,
    "Floods": 60,
    "Landslides": 50,
    "Severe Storms": 40,
    # EONET에서 제공하는 다른 카테고리들도 추가 가능
    "Sea and Lake Ice": 30,
    "Water Color": 20,
    "Dust and Haze": 25,
    "Temperature Extremes": 55,
    "Manmade": 10, # 인공 재해 (예: 오일 유출)
    "Drought": 65, # 가뭄
    # 추가적인 카테고리들...
}
DEFAULT_CATEGORY_WEIGHT = 20 # 목록에 없는 카테고리의 기본 점수

# 최근 발생 이벤트에 대한 추가 가중치
RECENCY_WEIGHTS = {
    "within_3_days": 20,
    "within_7_days": 10,
    "within_30_days": 5, # 예시: 한 달 이내 이벤트에도 약간의 가중치
}

def score_event(event):
    """
    주어진 이벤트 객체에 대해 위험도 점수를 계산합니다.

    Args:
        event (dict): 'category' (str)와 'date' (str, ISO 형식) 키를 포함하는 딕셔너리.

    Returns:
        int: 계산된 위험도 점수. 오류 발생 시 기본 점수 반환 가능.
    """
    category = event.get("category", "")
    event_date_str = event.get("date", "")
    
    current_score = 0

    # 1. 카테고리 기반 점수
    current_score += CATEGORY_WEIGHTS.get(category, DEFAULT_CATEGORY_WEIGHT)

    # 2. 발생 날짜 기반 점수 (최근일수록 가중치)
    if event_date_str:
        try:
            # ISO 8601 형식의 날짜 문자열 파싱 ('Z'는 UTC를 의미하며, fromisoformat이 처리 가능)
            event_dt = datetime.fromisoformat(event_date_str.replace("Z", "+00:00"))
            # event_dt가 timezone 정보가 없는 naive datetime일 경우, UTC로 가정
            if event_dt.tzinfo is None:
                event_dt = event_dt.replace(tzinfo=timezone.utc)

            now_utc = datetime.now(timezone.utc)
            days_difference = (now_utc - event_dt).days

            if days_difference <= 3:
                current_score += RECENCY_WEIGHTS["within_3_days"]
            elif days_difference <= 7:
                current_score += RECENCY_WEIGHTS["within_7_days"]
            elif days_difference <= 30: # 30일 이내 추가 가중치 (예시)
                current_score += RECENCY_WEIGHTS["within_30_days"]
            
            # 너무 오래된 이벤트는 감점할 수도 있음 (선택 사항)
            # elif days_difference > 365: # 1년 이상된 이벤트
            #     current_score -= 10 # 예시 감점

        except ValueError:
            print(f"날짜 형식 오류: '{event_date_str}'는 유효한 ISO 형식이 아닙니다. 날짜 기반 가중치를 적용하지 않습니다.")
        except Exception as e:
            print(f"날짜 처리 중 예외 발생: {e}. 날짜 기반 가중치를 적용하지 않습니다.")
    else:
        print("이벤트에 날짜 정보가 없어 날짜 기반 가중치를 적용하지 않습니다.")

    # 점수가 음수가 되지 않도록 보정 (만약 감점 로직이 있다면)
    final_score = max(0, current_score)
    
    # 최대 점수를 100으로 제한 (선택 사항, 정규화)
    # final_score = min(final_score, 100)

    return final_score

if __name__ == '__main__':
    # 테스트용 예시 이벤트
    example_event_recent_earthquake = {
        "category": "Earthquakes",
        "date": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat() # 1일 전
    }
    example_event_old_flood = {
        "category": "Floods",
        "date": (datetime.now(timezone.utc) - timedelta(days=10)).isoformat() # 10일 전
    }
    example_event_unknown_category = {
        "category": "UnknownDisaster",
        "date": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat() # 5일 전
    }
    example_event_no_date = {
        "category": "Volcanoes"
        # "date" 키 없음
    }
    example_event_invalid_date = {
        "category": "Wildfires",
        "date": "Not a valid date"
    }

    print(f"최근 지진 점수: {score_event(example_event_recent_earthquake)}")
    print(f"오래된 홍수 점수: {score_event(example_event_old_flood)}")
    print(f"알 수 없는 카테고리 점수: {score_event(example_event_unknown_category)}")
    print(f"날짜 없는 화산 점수: {score_event(example_event_no_date)}")
    print(f"잘못된 날짜 형식 산불 점수: {score_event(example_event_invalid_date)}")

    # EONET 카테고리 예시 테스트
    eonet_wildfire = {"category": "Wildfires", "date": "2023-10-27T10:30:00Z"}
    print(f"EONET 산불 (2023-10-27) 점수: {score_event(eonet_wildfire)}")
