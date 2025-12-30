# Global Disaster Risk Intelligence Platform (G-DRIP)

**엔터프라이즈급 실시간 상황 인식 및 예측적 위험 분석 시스템**

---

## 📋 경영 요약

**G-DRIP**은 전 세계 자연재해 데이터를 실시간으로 수집·분석하여 의사결정자에게 실행 가능한 인사이트를 제공하는 **미션 크리티컬 지리정보 인텔리전스 플랫폼**입니다. 

NASA EONET, GDACS, ReliefWeb 등 이종 데이터 소스를 단일 대시보드로 통합하여, 파편화된 정보를 **통합 상황 인식 환경**으로 전환합니다.

### 핵심 가치 제안
- **통합 관제 가시성**: 단일 접점에서 다중 도메인 재해 모니터링
- **AI 기반 위험 휴리스틱**: 독자적 알고리즘을 통한 지역별 위험 노출도 정량화
- **고정밀 시각화**: 직관적 위협 평가를 위한 대화형 지리정보 렌더링

---

## 🚀 핵심 역량

### 1. 다중 소스 데이터 수집 파이프라인
강력한 **ETL(Extract, Transform, Load)** 아키텍처를 기반으로 이종 소스의 비정형 데이터를 정규화합니다.

- **지구물리 원격 측정**: 실시간 지진 및 화산 활동 추적 (NASA EONET)
- **인도주의적 영향 지표**: 전염병 및 위기 경보 모니터링 (ReliefWeb)
- **글로벌 경보 프로토콜**: 표준화된 재난 이벤트 스트림 처리 (GDACS)

### 2. 예측 위험 분석 엔진 (PRAE)
원시 이벤트 데이터를 전략적 인텔리전스로 변환하는 **독립 분석 레이어**입니다.

- **공간 클러스터링 집계**: 고밀도 위협 지역(Hotspots)의 동적 식별
- **시계열 감쇠 모델링**: 최근 위협 우선순위화를 위한 가중치 스코어링
- **정량적 위험 지수**: 객관적 지역 비교를 위한 표준화된 0-100 스케일 산출

### 3. 엔터프라이즈 지리정보 인터페이스
- **계층화된 가시성**: 지진·기상·생물학적 위협 등 데이터 레이어 정밀 제어
- **맥락적 인텔리전스**: 기상 서비스 연동을 통한 국지적 상황 정보 제공
- **드릴다운 분석**: 이벤트 메타데이터 및 영향 평가 심층 검사

---

## 🏗 시스템 아키텍처

확장성과 유지보수성 보장을 위한 **마이크로 모듈러 아키텍처** 기반 설계

### 백엔드 인프라
- **핵심 런타임**: Python 3.x / Flask Framework
- **데이터 영속성**: SQLite (PostgreSQL/Oracle 마이그레이션 지원)
- **분석 모듈**: 위험 정량화 알고리즘 구현 `scorer` 모듈
- **연결성**: RESTful API/JSON 인터페이스

### 프론트엔드 클라이언트
- **프레임워크**: Modern ES6+ JavaScript
- **렌더링 엔진**: Leaflet.js 고성능 벡터 매핑
- **컴포넌트 설계**: 모듈식 UI/UX 매니저 (`mapManager`, `uiManager`)

---

## 💻 배포 가이드

### 사전 요구 사항
- Python 3.8+
- 의존성: `requirements.txt`
- OpenWeatherMap API 키 (필수)

### 설치 절차

**1. 리포지토리 초기화**
```bash
git clone [repository-url]
cd risk-map
pip install -r requirements.txt
```

**2. 환경 구성**
```python
# app_config.py
OPENWEATHER_API_KEY = "YOUR_API_KEY"
```

**3. 데이터베이스 초기화**
```bash
python database.py
```

**4. ETL 파이프라인 실행**
```bash
python modules/eonet_fetcher.py
python modules/gdacs_fetcher.py
python modules/disease_fetcher.py
```

**5. 서비스 시작**
```bash
python app.py
```
→ 관리 콘솔: `http://localhost:5000`

---

## 🧪 알고리즘 방법론: 지리공간 위험 정량화

**PRAE**는 결정론적 휴리스틱 모델을 통해 지역별 위험을 계산합니다.

### 계산 프로세스

**1. 이벤트 정규화**  
카테고리별 기본 심각도 가중치 부여 (지진: 90, 홍수: 60 등)

**2. 시계열 가중치**  
감쇠 함수를 통한 최신성 반영 (최근 72시간 내 우선순위)

**3. 공간 컨볼루션**  
지리공간 섹터 내 중첩 위협 벡터 집계

**4. 위험 등급 분류**
- **🔴 Critical (Deep Red)**: 300+
- **🔴 High (Red)**: 150+
- **🟠 Moderate (Orange)**: 80+
- **🟡 Monitor (Gold)**: 0+

---

## 🎯 AI 위험 분석 레이어: 시각화 가이드

### UI 인터페이스
컨트롤 패널에서 **🔥 AI 위험 분석** 토글을 활성화하면, 지도 위에 위험 구역이 **반투명 원형 영역**으로 표시됩니다.

### 시각적 요소 해석

**1. 원의 색상 = 위험 등급**
```
🔴 Deep Red (#800000)  → 극도로 위험 (점수 300+)
   예: 최근 대규모 지진 + 화산 활동 + 홍수가 동시 발생한 지역

🔴 Red (#FF0000)       → 높은 위험 (점수 150+)
   예: 여러 건의 중규모 재해가 반경 500km 내에 밀집

🟠 Orange (#FF8C00)    → 주의 필요 (점수 80+)
   예: 최근 한 달 내 산불/폭풍 등 재해 발생

🟡 Gold (#FFD700)      → 경계 상태 (점수 30+)
   예: 과거 이력이 있거나 낮은 수준의 활동 감지
```

**2. 원의 크기 = 영향 범위**
- 반경 약 500km (알고리즘 설정값)
- 실제로는 해당 격자 내 모든 이벤트를 포함하는 집계 영역

**3. 팝업 정보**
위험 구역 클릭 시 다음 정보 제공:
- **위험 점수**: 정량화된 수치 (예: 154)
- **이벤트 수**: 해당 지역에 집계된 재해 발생 건수
- **주요 요인**: 대표적인 재해 3가지 (예: "Earthquake near Tokyo", "Wildfire", "Flood")

---

## 🔬 AI 위험 분석 알고리즘: 완전 해부

본 시스템의 핵심인 **PRAE (Predictive Risk Analytics Engine)**는 총 **4단계 파이프라인**으로 구성됩니다.

---

### 🔢 Phase 0: 수학적 기초 - Haversine 거리 계산

지리공간 클러스터링의 기반이 되는 **구면 거리 계산 공식**입니다.

**Haversine Formula:**
```
d = 2R × arcsin(√(sin²(Δφ/2) + cos(φ₁) × cos(φ₂) × sin²(Δλ/2)))

여기서:
R  = 지구 반지름 (6371 km)
φ  = 위도 (latitude)
λ  = 경도 (longitude)
Δφ = φ₂ - φ₁
Δλ = λ₂ - λ₁
```

**Python 구현:**
```python
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
```

---

### 📊 Phase 1: 이벤트 정규화 및 스코어링

**1.1 카테고리 가중치 할당**

각 재해 유형의 **평균적 인명/재산 피해 규모**를 기반으로 가중치를 설계했습니다.

| 카테고리 | 가중치 | 근거 |
|----------|--------|------|
| Earthquakes | 90 | 대규모 구조물 붕괴, 2차 피해 (쓰나미) |
| Volcanoes | 80 | 광범위 화산재, 용암 흐름 |
| Wildfires | 70 | 급속 확산, 대기 오염 |
| Drought | 65 | 장기 식량/물 부족 |
| Floods | 60 | 침수 피해, 전염병 위험 |
| Temperature Extremes | 55 | 열사병/동사 위험 |
| Landslides | 50 | 국지적 매몰 |
| Severe Storms | 40 | 단기 피해 |
| Sea/Lake Ice | 30 | 항만 마비 |
| Dust and Haze | 25 | 호흡기 질환 |
| Water Color | 20 | 수질 오염 |
| Manmade | 10 | 통제 가능 |

**1.2 시간 감쇠 모델**

**지수 감쇠 개념**을 단순화한 계단식 함수:

```
Recency_Bonus(t) = {
    20,  if t ≤ 3   (days)
    10,  if 3 < t ≤ 7
    5,   if 7 < t ≤ 30
    0,   if t > 30
}

여기서 t = 현재 시간 - 이벤트 발생 시간
```

**1.3 통합 스코어 함수**

```python
def score_event(event):
    # Step 1: 카테고리 점수
    category = event.get('category', '')
    base_score = CATEGORY_WEIGHTS.get(category, 20)
    
    # Step 2: 시간 계산
    event_date = datetime.fromisoformat(event['date'])
    now = datetime.now(timezone.utc)
    days_diff = (now - event_date).days
    
    # Step 3: 감쇠 보너스
    if days_diff <= 3:
        bonus = 20
    elif days_diff <= 7:
        bonus = 10
    elif days_diff <= 30:
        bonus = 5
    else:
        bonus = 0
    
    # Step 4: 최종 점수
    final_score = max(0, base_score + bonus)
    return final_score
```

**예시 시나리오:**
```
[시나리오 1] 오늘 발생한 규모 7.5 지진
→ 90 (Earthquakes) + 20 (0일) = 110점

[시나리오 2] 5일 전 산불 발생
→ 70 (Wildfires) + 10 (5일) = 80점

[시나리오 3] 한 달 전 폭풍
→ 40 (Severe Storms) + 0 (30일+) = 40점
```

---

### 🗺️ Phase 2: 공간 집계 (Grid-Based Clustering)

**2.1 좌표 → 격자셀 변환**

**격자 인덱스 계산:**
```python
GRID_SIZE = 5  # degrees

def get_grid_cell(lat, lon):
    grid_lat = int(lat / GRID_SIZE)
    grid_lon = int(lon / GRID_SIZE)
    return (grid_lat, grid_lon)

# 예시
event_tokyo = {"lat": 35.68, "lon": 139.69}
cell = get_grid_cell(35.68, 139.69)
# → (7, 27)  # 격자 좌표
```

**격자 크기 실제 거리:**
```
위도 5° ≈ 5 × 111 km = 555 km (일정)
경도 5° ≈ 5 × 111 × cos(위도) km
  - 적도(0°): 555 km
  - 서울(37°): 443 km
  - 극지(80°): 96 km
```

**2.2 집계 알고리즘**

```python
def calculate_danger_zones(events):
    grid_map = {}  # {(grid_lat, grid_lon): 집계 데이터}
    
    # Step 1: 이벤트를 격자에 할당
    for event in events:
        lat, lon = event['latitude'], event['longitude']
        cell = get_grid_cell(lat, lon)
        score = score_event(event)
        
        if cell not in grid_map:
            grid_map[cell] = {
                'total_score': 0,
                'count': 0,
                'lat_sum': 0.0,
                'lon_sum': 0.0,
                'events': []
            }
        
        # 점수 합산
        grid_map[cell]['total_score'] += score
        grid_map[cell]['count'] += 1
        grid_map[cell]['lat_sum'] += lat
        grid_map[cell]['lon_sum'] += lon
        
        # 대표 이벤트 저장 (최대 3개)
        if len(grid_map[cell]['events']) < 3:
            grid_map[cell]['events'].append(event['title'])
    
    # Step 2: 무게중심 계산
    results = []
    for cell, data in grid_map.items():
        if data['total_score'] < 30:  # 노이즈 제거
            continue
        
        # 무게중심 좌표
        centroid_lat = data['lat_sum'] / data['count']
        centroid_lon = data['lon_sum'] / data['count']
        
        # 위험 등급 분류
        score = data['total_score']
        if score > 300:
            level = "DeepRed"
        elif score > 150:
            level = "High"
        elif score > 80:
            level = "Medium"
        else:
            level = "Low"
        
        results.append({
            'latitude': round(centroid_lat, 2),
            'longitude': round(centroid_lon, 2),
            'risk_score': score,
            'event_count': data['count'],
            'risk_level': level,
            'representative_events': data['events']
        })
    
    return results
```

**2.3 무게중심 (Centroid) 계산 원리**

점수를 고려하지 않은 **산술 평균 중심점**:

```
C_lat = (Σ lat_i) / n
C_lon = (Σ lon_i) / n

예시: 격자 내 3개 지진
- 지진1: (35.7, 139.8)
- 지진2: (35.6, 139.7)
- 지진3: (35.5, 140.0)

C_lat = (35.7 + 35.6 + 35.5) / 3 = 35.6
C_lon = (139.8 + 139.7 + 140.0) / 3 = 139.83
```

**향후 개선 방향**: 점수 가중 평균 (Weighted Centroid)
```
C_lat = Σ(score_i × lat_i) / Σ(score_i)
```

---

### 🎯 Phase 3: 위험 등급 분류

**분류 기준 설계 근거:**

| 등급 | 점수 | 시나리오 예시 |
|------|------|---------------|
| 🔴 **Critical** | 300+ | 3개 이상의 대규모 재해 동시 발생<br>(지진 110 + 화산 100 + 홍수 80 = 290+) |
| 🔴 **High** | 150+ | 2개의 주요 재해 중첩<br>(지진 110 + 산불 80 = 190) |
| 🟠 **Moderate** | 80+ | 1개의 최근 주요 재해<br>(지진 90 + 보너스 10 = 100) |
| 🟡 **Monitor** | 30+ | 복수의 경미한 재해 또는 단일 저위험 이벤트 |

---

### 🧮 Phase 4: 출력 정규화 및 API 응답

**최종 출력 형식:**
```json
[
  {
    "latitude": 35.68,
    "longitude": 139.69,
    "risk_score": 320,
    "event_count": 12,
    "risk_level": "DeepRed",
    "radius_km": 500,
    "representative_events": [
      "Earthquake M7.2 near Tokyo",
      "Volcanic eruption Mt. Fuji",
      "Severe flooding in Kanto"
    ]
  }
]
```

---

### ⚡ 성능 최적화 전략

**시간 복잡도:**
```
O(n) + O(m) = O(n + m)

n = 전체 이벤트 수
m = 고유 격자셀 수 (최대 64,800개 = 360°/5° × 180°/5°)
```

**공간 복잡도:**
```
O(m) ≈ O(격자 수)
실제로는 데이터가 있는 셀만 저장 (희소 행렬)
```

**데이터베이스 쿼리 최적화:**
```sql
-- app.py에서 실행되는 쿼리
SELECT id, title, category, date, longitude, latitude 
FROM eonet_events 
ORDER BY date DESC 
LIMIT 500
```
→ 최신 500개만 분석하여 응답 시간 < 1초 보장

---

### 🔮 알고리즘 확장 가능성

**현재 (v1.0):**
- 격자 기반 집계
- 규칙 기반 점수화
- 시간 감쇠 (계단 함수)

**향후 개선 방향 (v2.0):**
1. **DBSCAN 클러스터링**: 가변 크기 클러스터 지원
2. **가중치 학습**: 과거 피해 데이터 기반 ML 최적화
3. **시간 감쇠 개선**: 지수 함수 또는 시그모이드 적용
4. **재해 간 상관관계**: 지진 → 쓰나미 연쇄 반응 모델링
5. **인구 밀도 가중치**: 피해 예상 규모 정밀화

---

### 알고리즘 특징

✅ **투명성**: 블랙박스 ML이 아닌 해석 가능한 규칙 기반  
✅ **실시간성**: 데이터베이스 쿼리 후 즉시 계산 (< 1초)  
✅ **확장성**: 격자 크기/가중치 조정으로 민감도 제어 가능  
✅ **경량화**: 외부 AI 서비스 의존 없이 로컬에서 완결  
✅ **검증 가능성**: 모든 파라미터와 로직이 문서화되어 재현 가능

---

## 📊 데이터 소스

| 소스 | 용도 | URL |
|------|------|-----|
| NASA EONET | 자연재해 원격 측정 | [eonet.gsfc.nasa.gov](https://eonet.gsfc.nasa.gov/) |
| GDACS | 글로벌 재난 경보 | [gdacs.org](https://www.gdacs.org/) |
| ReliefWeb | 인도주의 위기 정보 | [reliefweb.int](https://reliefweb.int/) |
| OpenWeatherMap | 기상 데이터 연동 | [openweathermap.org](https://openweathermap.org/) |

---

## 📁 프로젝트 구조

```
risk-map/
├── app.py                      # Flask 서버 & API 엔드포인트
├── database.py                 # SQLite 연결 및 초기화
├── requirements.txt            # 의존성 패키지
├── data/
│   └── disaster_data.db        # 데이터 저장소
├── modules/
│   ├── scorer.py               # 위험 정량화 알고리즘 (Core)
│   ├── eonet_fetcher.py        # NASA 데이터 수집
│   ├── gdacs_fetcher.py        # GDACS 데이터 수집
│   ├── disease_fetcher.py      # 질병 데이터 수집
│   └── weather_fetcher.py      # 날씨 API 연동
├── static/
│   ├── css/style.css
│   └── js/
│       ├── main.js             # 앱 초기화
│       ├── riskLayer.js        # AI 위험 분석 레이어
│       ├── apiHandler.js       # 백엔드 통신
│       └── mapManager.js       # 지도 설정
└── templates/
    └── index.html              # 메인 인터페이스
```
