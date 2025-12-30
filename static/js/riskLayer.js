// static/js/riskLayer.js

// AI 위험 분석 레이어 관리 모듈
// 백엔드에서 계산된 위험 구역(Risk Zones)을 시각화합니다.

let riskLayerGroup = L.layerGroup();
let isLayerVisible = false;

// 위험도에 따른 색상 반환
function getRiskColor(score) {
  if (score > 300) return "#800000"; // Deep Red (매우 심각)
  if (score > 150) return "#FF0000"; // Red (높음)
  if (score > 80) return "#FF8C00"; // Dark Orange (중간)
  return "#FFD700"; // Gold (낮음/주의)
}

// 위험 분석 데이터 로드 및 시각화
export async function loadRiskAnalysisLayer(map) {
  if (isLayerVisible) return; // 이미 로드됨

  try {
    const response = await fetch("/api/risk-analysis");
    const data = await response.json();

    if (data.error) {
      console.error("위험 분석 데이터 오류:", data.error);
      return;
    }

    // 기존 레이어 초기화
    riskLayerGroup.clearLayers();

    data.forEach((zone) => {
      const {
        latitude,
        longitude,
        risk_score,
        event_count,
        radius_km,
        representative_events,
      } = zone;

      // 원형 마커 생성
      // radius는 미터 단위이므로 km * 1000
      // 시각적 효과를 위해 점수에 따라 투명도나 크기를 조절할 수도 있음
      const circle = L.circle([latitude, longitude], {
        color: getRiskColor(risk_score),
        fillColor: getRiskColor(risk_score),
        fillOpacity: 0.4,
        radius: radius_km * 1000 * 0.8, // 겹침 방지를 위해 약간 축소
        weight: 1,
      });

      // 팝업/툴팁 내용 구성
      const popupContent = `
                <div class="risk-popup">
                    <h4>🔥 AI 위험 구역</h4>
                    <p><strong>위험 점수:</strong> ${risk_score.toFixed(0)}</p>
                    <p><strong>이벤트 수:</strong> ${event_count}건</p>
                    <hr>
                    <p class="subtitle">주요 요인:</p>
                    <ul>
                        ${representative_events
                          .map((t) => `<li>${t}</li>`)
                          .join("")}
                    </ul>
                </div>
            `;

      circle.bindPopup(popupContent);
      riskLayerGroup.addLayer(circle);
    });

    // 지도에 레이어 추가
    riskLayerGroup.addTo(map);
    isLayerVisible = true;
    console.log(`[RiskLayer] ${data.length}개 위험 구역 로드 완료`);
  } catch (error) {
    console.error("위험 분석 데이터 로드 실패:", error);
  }
}

// 레이어 숨기기
export function removeRiskAnalysisLayer(map) {
  if (!isLayerVisible) return;

  map.removeLayer(riskLayerGroup);
  isLayerVisible = false;
}
