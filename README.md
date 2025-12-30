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

## 🔬 알고리즘 상세 메커니즘

### Phase 1: 이벤트 스코어링 (Event Scoring)

각 재해 이벤트는 다음 공식으로 점수화됩니다:

```python
Event_Score = Base_Weight + Recency_Bonus
```

**Base Weight 매트릭스:**
```
Earthquakes      : 90   # 가장 높은 위험도
Volcanoes        : 80
Wildfires        : 70
Drought          : 65
Floods           : 60
Temperature Ext. : 55
Landslides       : 50
Severe Storms    : 40
Dust and Haze    : 25
Default          : 20
```

**Recency Bonus (시간 감쇠):**
```
현재로부터 3일 이내   : +20점
현재로부터 7일 이내   : +10점
현재로부터 30일 이내  : +5점
30일 초과            : 0점
```

**예시 계산:**
- 2일 전 발생한 지진 → 90 (Base) + 20 (Recency) = **110점**
- 15일 전 발생한 홍수 → 60 (Base) + 0 = **60점**

---

### Phase 2: 공간 집계 (Spatial Aggregation)

**그리드 기반 클러스터링:**
1. 전 세계를 **5도 × 5도 격자**로 분할
   - 위도 5도 ≈ 약 555km
   - 적도 기준 경도 5도 ≈ 약 555km

2. 각 격자 셀에 속한 모든 이벤트의 점수를 **합산**
   ```
   Grid_Risk_Score = Σ(Event_Score_i)
   ```

3. 격자 내 이벤트 좌표의 **무게중심(Centroid)** 계산
   ```
   Centroid_Lat = Σ(lat_i) / n
   Centroid_Lon = Σ(lon_i) / n
   ```

---

### Phase 3: 필터링 및 정규화

**노이즈 제거:**
- 점수가 30점 미만인 격자는 제외 (단일 저위험 이벤트 필터링)

**결과 출력:**
```json
{
  "latitude": 35.68,
  "longitude": 139.69,
  "risk_score": 245,
  "event_count": 8,
  "risk_level": "High",
  "representative_events": [
    "Earthquake M6.8 near Tokyo",
    "Volcanic activity detected",
    "Flood alert issued"
  ]
}
```

---

### 알고리즘 특징

✅ **투명성**: 블랙박스 ML이 아닌 해석 가능한 규칙 기반  
✅ **실시간성**: 데이터베이스 쿼리 후 즉시 계산 (< 1초)  
✅ **확장성**: 격자 크기/가중치 조정으로 민감도 제어 가능  
✅ **경량화**: 외부 AI 서비스 의존 없이 로컬에서 완결

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
