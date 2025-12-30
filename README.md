# Global Disaster Risk Intelligence Platform (G-DRIP)

**엔터프라이즈급 실시간 상황 인식 및 예측적 위험 분석 시스템**

---

## 📋 경영 요약 (Executive Summary)
**G-DRIP**은 전 세계의 자연재해 데이터를 실시간으로 수집, 통합, 분석하여 의사결정자에게 실행 가능한 인사이트를 제공하는 **미션 크리티컬 지리정보 인텔리전스 플랫폼**입니다. 
NASA EONET, GDACS, ReliefWeb 등 이종(Heterogeneous) 데이터 소스를 단일 대시보드로 통합하여, 파편화된 정보를 **통합 상황 인식(Situational Awareness)** 환경으로 전환합니다.

핵심 가치 제안:
- **통합 관제 가시성**: 단일 접점(Single-pane-of-glass)에서 다중 도메인 재해 모니터링.
- **AI 기반 위험 휴리스틱**: 독자적인 알고리즘을 통한 지역별 위험 노출도 정량화.
- **고정밀 시각화**: 직관적인 위협 평가를 위한 대화형 지리정보 렌더링.

---

## 🚀 핵심 역량 (Key Capabilities)

### 1. 다중 소스 데이터 수집 파이프라인 (Multi-Source Ingestion Pipeline)
이 플랫폼은 다양한 소스의 비정형 데이터를 정규화하기 위해 강력한 **ETL (Extract, Transform, Load)** 아키텍처를 구현합니다:
- **지구물리 원격 측량 (Geophysical Telemetry)**: 실시간 지진 및 화산 활동 추적 (NASA EONET).
- **인도주의적 영향 지표**: 전염병 및 위기 경보 모니터링 (ReliefWeb).
- **글로벌 경보 프로토콜**: 표준화된 재난 이벤트 스트림 처리 (GDACS).

### 2. 예측 위험 분석 엔진 (PRAE - Predictive Risk Analytics Engine)
수집된 원시 이벤트 데이터를 전략적 인텔리전스로 변환하는 독립 분석 레이어입니다:
- **공간 클러스터링 집계**: 고밀도 위협 지역(Hotspots)의 동적 식별.
- **시계열 감쇠 모델링**: 과거 데이터보다 최근의 위협에 우선순위를 부여하는 가중치 스코어링 ($T_{delta}$).
- **정량적 위험 스코어링**: 객관적인 지역 비교를 위한 표준화된 0-100 위험 지수 산출.

### 3. 엔터프라이즈 지리정보 인터페이스
- **계층화된 가시성 (Layered Visibility)**: 지진, 기상, 생물학적 위협 등 데이터 레이어에 대한 정밀 제어.
- **맥락적 인텔리전스**: 기상 서비스(OpenWeatherMap)와의 온디맨드 연동을 통한 국지적 상황 정보 제공.
- **드릴다운 분석 (Drill-Down Analytics)**: 이벤트 메타데이터 및 영향 평가에 대한 심층 검사 기능.

---

## 🏗 시스템 아키텍처

본 솔루션은 확장성과 유지보수성을 보장하기 위해 마이크로 모듈러(Micro-modular) 아키텍처를 채택했습니다.

### 백엔드 인프라 (Backend)
- **핵심 런타임**: Python 3.x / Flask Framework.
- **데이터 영속성**: SQLite (엔터프라이즈 배포 시 PostgreSQL/Oracle 마이그레이션 지원).
- **분석 모듈**: **위험 정량화 알고리즘**을 구현한 독립적인 `scorer` 모듈.
- **연결성**: 프론트엔드와의 결합 분리를 위한 RESTful API/JSON 인터페이스.

### 프론트엔드 클라이언트 (Frontend)
- **프레임워크**: Modern ES6+ JavaScript Architecture.
- **렌더링 엔진**: 고성능 벡터 매핑을 위한 Leaflet.js.
- **컴포넌트 설계**: 빠른 기능 확장을 지원하는 모듈식 UI/UX 매니저 (`mapManager`, `uiManager`).

---

## 💻 배포 및 운영 가이드

### 사전 요구 사항
- **런타임 환경**: Python 3.8 이상
- **의존성 라이브러리**: `requirements.txt` 명시
- **외부 연동**: OpenWeatherMap API 자격 증명 (기상 컨텍스트용, 필수).

### 설치 절차

1.  **리포지토리 초기화**
    ```bash
    git clone [repository-url]
    cd risk-map-project
    pip install -r requirements.txt
    ```

2.  **환경 구성**
    `app_config.py`를 편집하여 환경 변수 및 API 키를 주입합니다.

3.  **데이터 웨어하우스 프로비저닝**
    스키마 및 로컬 데이터 저장소를 초기화합니다:
    ```bash
    python database.py
    ```

4.  **ETL 파이프라인 실행**
    데이터 수집 모듈을 트리거하여 웨어하우스를 채웁니다:
    ```bash
    python modules/eonet_fetcher.py
    python modules/gdacs_fetcher.py
    python modules/disease_fetcher.py
    ```

5.  **서비스 활성화**
    애플리케이션 서버를 구동합니다:
    ```bash
    python app.py
    ```
    관리 콘솔(`http://localhost:5000`)에 접속합니다.

---

## 🧪 알고리즘 방법론: 지리공간 위험 정량화

**예측 위험 분석 엔진(PRAE)**은 지역적 위험 노출을 계산하기 위해 다음과 같은 결정론적 휴리스틱 모델을 사용합니다:

1.  **이벤트 정규화**: 수집된 이벤트는 카테고리화되어 **기본 심각도 가중치(Base Severity Weight)**가 부여됩니다 (예: 지진 90, 홍수 60).
2.  **시계열 가중치 적용**: 감쇠 함수(Decay Function)를 통해 이벤트 최신성($T_{delta}$)에 따른 승수를 적용하여, 최근 72시간 내의 활동에 우선순위를 둡니다.
3.  **공간 컨볼루션 (Spatial Convolution)**: 정의된 지리공간 섹터(Grid/Radius) 내에서 중첩되는 위협 벡터를 집계하여 누적 위험 점수를 계산합니다.
4.  **위험 등급 분류**:
    - **치명적 (Critical / Deep Red)**: 점수 > 300
    - **고위험 (High / Red)**: 점수 > 150
    - **주의 (Moderate / Orange)**: 점수 > 80
    - **관찰 (Monitor / Gold)**: 점수 > 0

---

## 🛡 면책 조항
*본 플랫폼은 정보 제공 목적으로 공개 도메인 데이터를 집계합니다. 공식적인 정부 경보 시스템이나 비상 방송 네트워크를 대체할 의도로 제작되지 않았습니다.*
