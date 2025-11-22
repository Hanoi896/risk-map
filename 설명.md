# 🌍 글로벌 자연재해 위험도 시각화 프로젝트

## 📖 프로젝트 개요
이 프로젝트는 전 세계에서 발생하는 다양한 자연재해(지진, 화산, 홍수, 질병 등) 데이터를 실시간으로 수집하여 인터랙티브 지도 위에 시각화하는 웹 애플리케이션입니다. 
사용자는 지도에서 재해의 위치, 상세 정보, 위험도를 한눈에 파악할 수 있으며, 특정 위치를 클릭하여 해당 지역의 실시간 날씨 정보도 확인할 수 있습니다.

---

## 🛠 기술 스택

### Backend (Python)
- **Flask**: 경량 웹 서버 프레임워크. API 라우팅 및 정적 파일 제공.
- **SQLite**: 수집된 데이터를 영구 저장하는 파일 기반 관계형 데이터베이스.
- **Requests**: 외부 API(NASA, ReliefWeb 등) 데이터 요청.
- **xmltodict**: GDACS RSS(XML) 데이터 파싱.

### Frontend (JavaScript)
- **Leaflet.js**: 오픈소스 인터랙티브 지도 라이브러리.
- **Leaflet Control Geocoder**: 지도 내 주소 검색 기능.
- **ES6 Modules**: 유지보수성을 위한 기능별 코드 모듈화 (`mapManager`, `uiManager` 등).
- **CSS3**: 직관적인 UI/UX 디자인 (패널 슬라이드, 토글 스위치 등).
=========================================================================================================
map-visualizer/
├── app.py                  # [Main] Flask 웹 서버. API 요청 처리 및 응답.
├── app_config.py           # [Config] API 키 및 URL 상수 관리.
├── database.py             # [DB] 데이터베이스 연결 및 초기 테이블 생성 스크립트.
├── db_manager.py           # [DB] 데이터 조회(SELECT) 및 저장(INSERT) 로직 분리.
├── requirements.txt        # [Env] 필요한 Python 패키지 목록.
├── data/
│   └── disaster_data.db    # [Data] 재해 데이터가 저장되는 SQLite DB 파일.
├── modules/                # [Backend] 데이터 수집 스크립트 (Fetcher)
│   ├── eonet_fetcher.py    # NASA EONET 데이터 수집.
│   ├── gdacs_fetcher.py    # GDACS RSS 데이터 파싱 및 수집.
│   ├── disease_fetcher.py  # ReliefWeb 질병 데이터 수집.
│   ├── weather_fetcher.py  # 특정 좌표 날씨 조회 (실시간).
│   └── scorer.py           # 재해 위험도 점수 계산 로직.
├── static/
│   ├── css/
│   │   └── style.css       # [Frontend] UI 스타일링.
│   └── js/                 # [Frontend] JS 모듈
│       ├── main.js         # 앱 초기화 진입점.
│       ├── apiHandler.js   # 백엔드 API 통신 담당.
│       ├── config.js       # 아이콘, 색상 등 설정값.
│       ├── mapManager.js   # 지도 객체 및 타일 설정.
│       ├── uiManager.js    # UI 이벤트(버튼, 필터) 핸들링.
│       └── markerManager.js# 마커 생성 및 삭제 로직.
└── templates/
    └── index.html          # [View] 메인 HTML 페이지.
  ====================================================================================================
  ⚙️ 설치 및 실행 방법
1. 필수 패키지 설치
프로젝트 실행에 필요한 Python 라이브러리를 설치합니다.
code
Bash
pip install -r requirements.txt
(주요 패키지: Flask, requests, xmltodict)
2. API 키 설정
app_config.py 파일을 열어 OpenWeatherMap API 키를 설정해야 날씨 기능이 작동합니다.
code
Python
# app_config.py
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
3. 데이터베이스 초기화
최초 실행 시 데이터베이스 파일과 테이블을 생성합니다.
code
Bash
python database.py
4. 데이터 수집 (Fetcher 실행)
각 데이터 소스별로 스크립트를 실행하여 DB에 데이터를 채웁니다. (초기 1회 필수, 이후 주기적으로 실행 권장)
code
Bash
# NASA EONET 데이터 (시간이 조금 걸릴 수 있음)
python modules/eonet_fetcher.py

# GDACS 데이터
python modules/gdacs_fetcher.py

# ReliefWeb 질병 데이터
python modules/disease_fetcher.py
5. 웹 서버 실행
Flask 애플리케이션을 실행합니다.
code
Bash
python app.py
6. 접속
웹 브라우저를 열고 아래 주소로 접속합니다.
URL: http://localhost:5000
====================================================================================================
📊 데이터 소스 및 API 정보
데이터 소스	용도	데이터 형식	인증 필요 여부	비고
NASA EONET	자연재해 (산불, 화산 등)	JSON	No	대량 데이터 요청 시 연도별 분할 수집
GDACS	국제 재난 경보 (지진, 태풍)	RSS (XML)	No	xmltodict로 파싱하여 사용
ReliefWeb	질병 발생 및 인도주의 위기	JSON	No	검색 쿼리 및 필터 사용
OpenWeatherMap	실시간 날씨 정보	JSON	Yes (API Key)	지도 클릭 시 해당 좌표 날씨 제공
====================================================================================================
사용 방법
레이어 토글: 화면 좌측 상단 '컨트롤 패널' 버튼을 눌러 패널을 엽니다. EONET, GDACS, 질병 정보 레이어를 켜고 끌 수 있습니다. (EONET은 기본적으로 꺼져 있습니다.)
필터링: EONET 데이터의 경우 연도와 카테고리를 선택하여 원하는 데이터만 지도에 표시할 수 있습니다.
상세 정보: 지도에 표시된 마커를 클릭하면 재해의 상세 정보(날짜, 위험도 점수, 원본 링크 등)가 팝업으로 뜹니다.
날씨 확인: 지도의 빈 곳이나 특정 지역을 클릭하면 해당 위치의 현재 날씨(온도, 습도, 풍속) 팝업이 나타납니다.
주소 검색: 지도 우측 상단의 돋보기 아이콘을 통해 특정 지역으로 이동할 수 있습니다.
====================================================================================================
유지보수 참고사항
데이터 갱신: 실시간 데이터를 유지하려면 서버에서 cron 등을 이용해 modules/ 폴더 내의 fetcher 스크립트들을 주기적으로 실행해야 합니다.
DB 관리: 데이터가 data/disaster_data.db에 계속 누적되므로, 주기적으로 오래된 데이터를 정리하거나 백업하는 것이 좋습니다.
API 제한: OpenWeatherMap 무료 플랜 등 API 호출 제한이 있는 서비스 사용 시 주의가 필요합니다.
