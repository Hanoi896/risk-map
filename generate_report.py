from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# 한글 폰트 등록 (Windows 기본 폰트)
try:
    pdfmetrics.registerFont(TTFont('Malgun', 'malgun.ttf'))
    pdfmetrics.registerFont(TTFont('MalgunBold', 'malgunbd.ttf'))
    korean_font = 'Malgun'
    korean_font_bold = 'MalgunBold'
except:
    # 폰트 파일을 찾을 수 없는 경우 시스템 폰트 경로 사용
    font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    pdfmetrics.registerFont(TTFont('Malgun', os.path.join(font_path, 'malgun.ttf')))
    pdfmetrics.registerFont(TTFont('MalgunBold', os.path.join(font_path, 'malgunbd.ttf')))
    korean_font = 'Malgun'
    korean_font_bold = 'MalgunBold'

# PDF 파일 생성
pdf_filename = "프로젝트_보고서.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)

# 스토리 컨테이너
story = []

# 커스텀 스타일 정의
styles = getSampleStyleSheet()

# 제목 스타일
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontName=korean_font_bold,
    fontSize=24,
    textColor='#1a1a1a',
    spaceAfter=30,
    alignment=TA_CENTER,
    leading=30
)

# 섹션 제목 스타일
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontName=korean_font_bold,
    fontSize=16,
    textColor='#2c3e50',
    spaceAfter=12,
    spaceBefore=20,
    leading=20
)

# 본문 스타일
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontName=korean_font,
    fontSize=11,
    textColor='#333333',
    alignment=TA_JUSTIFY,
    spaceAfter=12,
    leading=18
)

# 리스트 스타일
list_style = ParagraphStyle(
    'CustomList',
    parent=styles['BodyText'],
    fontName=korean_font,
    fontSize=10,
    textColor='#444444',
    leftIndent=20,
    spaceAfter=8,
    leading=16
)

# === 콘텐츠 작성 ===

# 1. 메인 제목
story.append(Paragraph("Global Disaster Risk Intelligence Platform (G-DRIP)", title_style))
story.append(Paragraph("전 세계 자연재해 위험 시각화 프로젝트", heading_style))
story.append(Spacer(1, 0.3 * inch))

# 2. 제작한 내용
story.append(Paragraph("📋 제작한 내용", heading_style))

content_intro = """
본 프로젝트는 NASA EONET, GDACS, ReliefWeb 등 전 세계 재난 데이터 소스를 통합하여 실시간으로 
자연재해를 시각화하는 웹 기반 인텔리전스 플랫폼입니다. 엔터프라이즈급 시스템 아키텍처를 
적용하여 의사결정자에게 실행 가능한 인사이트를 제공하는 것을 목표로 개발되었습니다.
"""
story.append(Paragraph(content_intro, body_style))
story.append(Spacer(1, 0.15 * inch))

# 주요 기능
story.append(Paragraph("<b>핵심 기능 및 시스템 구성</b>", body_style))
features = [
    "• <b>다중 소스 데이터 통합:</b> NASA EONET(지진, 화산), GDACS(글로벌 재난 경보), ReliefWeb(인도주의 위기) 등 이종 데이터를 실시간으로 수집하고 정규화",
    "• <b>AI 기반 위험 분석 엔진 (PRAE):</b> 독자 개발한 알고리즘을 통해 재해 밀집도와 시간 감쇠 모델을 적용, 지역별 위험 점수(0-100 스케일)를 자동 산출",
    "• <b>지리정보 시각화:</b> Leaflet.js 기반 대화형 지도에 재해 이벤트와 AI 분석 위험 구역을 계층별로 표시",
    "• <b>실시간 기상 정보:</b> OpenWeatherMap API 연동으로 클릭한 위치의 현재 날씨 정보 제공",
    "• <b>모듈러 아키텍처:</b> Python Flask 백엔드, SQLite 데이터베이스, ES6+ JavaScript 프론트엔드로 구성된 확장 가능한 시스템",
]
for feature in features:
    story.append(Paragraph(feature, list_style))

story.append(Spacer(1, 0.15 * inch))

tech_stack = """
<b>기술 스택:</b> Python 3.x + Flask (백엔드), SQLite (데이터베이스), Leaflet.js (지도 렌더링), 
Vanilla JavaScript ES6+ (프론트엔드), RESTful API 설계
"""
story.append(Paragraph(tech_stack, body_style))

# 3. 문제 극복 과정
story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("🔧 문제 극복 과정", heading_style))

challenges = [
    {
        "title": "1. 이종 데이터 소스 통합 문제",
        "problem": "NASA EONET, GDACS, ReliefWeb는 각각 JSON 구조, 업데이트 주기, 좌표 형식이 상이하여 직접적인 통합이 불가능했습니다.",
        "solution": "각 소스별 전용 fetcher 모듈(eonet_fetcher.py, gdacs_fetcher.py, disease_fetcher.py)을 개발하여 데이터를 표준화된 스키마로 변환 후 단일 데이터베이스에 저장하는 ETL 파이프라인을 구축했습니다."
    },
    {
        "title": "2. AI 위험 분석 알고리즘 설계",
        "problem": "단순 재해 마커 표시를 넘어 '어느 지역이 위험한가'를 정량화하는 알고리즘이 필요했으나, 기존 오픈소스에는 이러한 기능이 없었습니다.",
        "solution": "격자 기반 클러스터링(Grid-Based Clustering)과 시간 감쇠 모델을 결합한 독자적인 위험 스코어링 시스템을 개발했습니다. 재해 카테고리별 가중치, 발생 시점 기반 감쇠 보너스, Haversine 거리 계산을 적용하여 지역별 위험도를 0-100 스케일로 산출합니다."
    },
    {
        "title": "3. 프론트엔드-백엔드 비동기 통신 최적화",
        "problem": "500개 이상의 재해 데이터와 AI 분석 결과를 동시에 로드할 때 초기 로딩 시간이 3초 이상 소요되었습니다.",
        "solution": "API 엔드포인트를 기능별로 분리(/api/disasters, /api/risk-analysis)하고, 프론트엔드에서 Promise.all()을 사용한 병렬 요청으로 로딩 시간을 1초 이내로 단축했습니다. 또한 데이터베이스 쿼리를 최신 500건으로 제한하는 최적화를 적용했습니다."
    },
    {
        "title": "4. 한글 문서화 및 전문성 강화",
        "problem": "초기 README는 기능 나열 수준이었으나, 프로젝트의 기술적 깊이를 충분히 전달하지 못했습니다.",
        "solution": "엔터프라이즈급 문서 구조를 채택하여 '경영 요약', '시스템 아키텍처', '알고리즘 방법론' 섹션을 추가하고, 수학 공식과 코드 예시를 포함한 상세한 기술 문서를 작성했습니다."
    }
]

for challenge in challenges:
    story.append(Paragraph(f"<b>{challenge['title']}</b>", body_style))
    story.append(Paragraph(f"<i>문제:</i> {challenge['problem']}", list_style))
    story.append(Paragraph(f"<i>해결:</i> {challenge['solution']}", list_style))
    story.append(Spacer(1, 0.1 * inch))

# 4. 소감
story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("💭 소감", heading_style))

reflection = """
이번 프로젝트를 통해 단순한 데이터 시각화를 넘어 실제 사회적 가치를 제공할 수 있는 시스템을 
설계하는 경험을 할 수 있었습니다. 특히 세 가지 측면에서 큰 성장을 느꼈습니다.
"""
story.append(Paragraph(reflection, body_style))

reflections = [
    "• <b>시스템 통합 역량:</b> 여러 외부 API를 통합하면서 데이터 정규화, 에러 핸들링, 스케줄링 등 실무 엔지니어링 스킬을 체득했습니다. 특히 각 API의 rate limit과 응답 형식 차이를 고려한 설계의 중요성을 깨달았습니다.",
    "• <b>알고리즘 설계 능력:</b> Haversine 거리 계산, 격자 기반 클러스터링, 시간 감쇠 모델 등 지리공간 분석 알고리즘을 직접 구현하며 이론과 실무의 간극을 메우는 법을 배웠습니다. 특히 '해석 가능한 AI'의 가치를 실감했습니다.",
    "• <b>문서화의 중요성:</b> 코드만큼이나 문서화가 프로젝트의 완성도를 좌우한다는 것을 배웠습니다. 기술적 깊이를 전달하면서도 비전문가도 이해할 수 있는 균형 잡힌 문서 작성이 얼마나 어려운지 알게 되었습니다.",
]
for ref in reflections:
    story.append(Paragraph(ref, list_style))

story.append(Spacer(1, 0.15 * inch))

conclusion = """
향후에는 머신러닝 기반 재해 예측, 인구 밀도를 고려한 피해 규모 추정, 실시간 알림 시스템 등으로 
확장하여 실제 재난 대응 기관에서 활용 가능한 수준의 플랫폼으로 발전시키고 싶습니다. 
이번 프로젝트는 단순한 과제를 넘어 제 커리어의 포트폴리오 핵심 프로젝트가 될 것입니다.
"""
story.append(Paragraph(conclusion, body_style))

# PDF 생성
doc.build(story)
print(f"✅ PDF 보고서가 생성되었습니다: {pdf_filename}")
print(f"📄 파일 경로: {os.path.abspath(pdf_filename)}")
