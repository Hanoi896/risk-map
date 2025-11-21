// static/js/main.js
import { 
  fetchWeather, 
  getEonetData, 
  getGdacsData,
  getDiseaseData
} from './apiHandler.js';

const map = L.map('map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
L.Control.geocoder({ defaultMarkGeocode: true }).addTo(map);

// 아이콘 정의
const disasterIcons = {
'Volcanoes': '🌋', 'Earthquakes': '🌐', 'Wildfires': '🔥', 'Floods': '🌊',
'Drought': '🌵', 'Severe Storms': '⛈️', 'Landslides': '⛰️', 
'Sea and Lake Ice': '🧊', 'Water Color': '💧', 'Dust and Haze': '🌫️',
'Temperature Extremes': '🌡️', 'Manmade': '🏭',
'Tropical Cyclone': '🌀', // GDACS
'Disease Outbreak': '🦠', // Disease
'Disaster': '📢', // GDACS 기본
'Default': '❗' // EONET 기본
};

// --- 마커 관리 배열 ---
let eonetMarkers = [];
let gdacsMarkers = [];
let diseaseMarkers = [];

// --- 마커 클리어 함수 ---
function clearMarkers(markerArray) {
markerArray.forEach(marker => map.removeLayer(marker));
markerArray.length = 0; 
}

// --- EONET ---
function getEonetColorByScore(score) {
if (score >= 90) return '#ff0000'; if (score >= 70) return '#ff6600';
if (score >= 50) return '#ffcc00'; if (score >= 30) return '#99cc00';
if (score > 0) return '#33cc33'; return '#999999';
}
async function loadAndDisplayEonet() {
  clearMarkers(eonetMarkers);
  if (!document.getElementById('toggle-eonet')?.checked) {
    console.log("EONET 레이어 꺼짐. 마커를 표시하지 않습니다.");
    return;
  }
  console.log("EONET 데이터 로딩 중 (서버 필터링)...");
  const yearFilterValue = document.getElementById('year-filter').value;
  const categoryFilterValue = document.getElementById('category-filter').value;
  let apiUrl = '/api/eonet';
  const params = new URLSearchParams();
  if (yearFilterValue) { params.append('year', yearFilterValue); }
  if (categoryFilterValue) { params.append('category', categoryFilterValue); }
  const queryString = params.toString();
  if (queryString) { apiUrl += `?${queryString}`; }

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: `HTTP 오류: ${response.status}` }));
        alert(`EONET 데이터 로드 실패: ${errorData.error || response.statusText}`); return;
    }
    const events = await response.json();
    if (events.error) { alert(`EONET 오류: ${events.error}`); return; }
    if (!Array.isArray(events)) { alert("EONET 데이터 형식이 잘못되었습니다 (배열이 아님)."); return; }
  
    events.forEach(event => { 
        if (!event.latitude || !event.longitude) { return; }
        const icon = disasterIcons[event.category] || disasterIcons.Default;
        const marker = L.circleMarker([event.latitude, event.longitude], {
            radius: 8, fillColor: getEonetColorByScore(event.score), color: '#000', weight: 1, fillOpacity: 0.8
        }).addTo(map);
        marker.bindPopup(`<h4>${icon} ${event.title}</h4><p>📅 ${new Date(event.date).toLocaleDateString('ko-KR')}</p><p>⭐ 점수: ${event.score ?? 'N/A'}</p><p>🗂️ 카테고리: ${event.category}</p><p><em>출처: EONET</em></p>`);
        eonetMarkers.push(marker);
    });
    console.log(`EONET 이벤트 ${events.length}개 표시 완료 (서버 필터링).`);
  } catch (error) {
      console.error("EONET 데이터 요청/처리 중 오류:", error);
      alert("EONET 데이터를 가져오는 중 오류가 발생했습니다.");
  }
}

// --- GDACS ---
function getGdacsColor(level) {
  if (!level) return '#808080'; // 기본 회색
  switch (level.toLowerCase()) {
    case 'red': return '#FF0000';
    case 'orange': return '#FFA500';
    case 'green': return '#00C800';
    default: return '#808080';
  }
}

async function loadAndDisplayGdacs() { // <<< 여기가 추가된 함수
  clearMarkers(gdacsMarkers);
  if (!document.getElementById('toggle-gdacs')?.checked) {
    console.log("GDACS 레이어 꺼짐. 마커를 표시하지 않습니다.");
    return;
  }
  console.log("GDACS 데이터 로딩 중...");
  
  try {
    const events = await getGdacsData(); // apiHandler.js의 함수 호출
    if (events.error) { 
      alert(`GDACS 오류: ${events.error}`); 
      console.error("GDACS 데이터 로드 오류:", events.error);
      return; 
    }
    if (!Array.isArray(events)) {
      alert("GDACS 데이터 형식이 잘못되었습니다 (배열이 아님).");
      console.error("GDACS 데이터 형식이 배열이 아님:", events);
      return;
    }

    events.forEach(event => {
      if (!event.latitude || !event.longitude) {
          return;
      }
      const icon = disasterIcons[event.category] || disasterIcons[event.original_category_code] || disasterIcons.Disaster;
      const marker = L.circleMarker([event.latitude, event.longitude], {
        radius: 7, 
        fillColor: getGdacsColor(event.alert_level), 
        color: '#FFFFFF', // 흰색 테두리
        weight: 1.5, 
        fillOpacity: 0.85
      }).addTo(map);

      const safeTitle = event.title?.replace(/</g, "<") || "제목 없음";
      const safeDesc = event.description?.replace(/</g, "<")?.substring(0,150) || "";

      marker.bindPopup(
        `<h4>${icon} ${safeTitle}</h4>
         <p>📅 ${new Date(event.date).toLocaleString('ko-KR', {dateStyle: 'medium', timeStyle: 'short'})}</p>
         <p>🚨 경보: ${event.alert_level || 'N/A'}</p>
         <p>🗂️ 카테고리: ${event.category}</p>
         ${event.country ? `<p>🌍 국가: ${event.country}</p>`:''}
         ${safeDesc ? `<p>📄 개요: ${safeDesc}...</p>` : ''}
         ${event.link ? `<p><a href="${event.link}" target="_blank" rel="noopener noreferrer">상세 정보</a></p>` : ''}
         <p><em>출처: GDACS</em></p>`
      );
      gdacsMarkers.push(marker);
    });
    console.log(`GDACS 이벤트 ${events.length}개 표시 완료.`);
  } catch (error) {
    console.error("GDACS 데이터 요청/처리 중 오류:", error);
    alert("GDACS 데이터를 가져오는 중 오류가 발생했습니다.");
  }
}

// --- 질병 발생 (Disease) ---
async function loadAndDisplayDisease() { // <<< 여기가 추가된 함수
  clearMarkers(diseaseMarkers);
  if (!document.getElementById('toggle-disease')?.checked) {
    console.log("질병 발생 레이어 꺼짐. 마커를 표시하지 않습니다.");
    return;
  }
  
  const countryQuery = ""; // 필요시 UI에서 국가 필터 값 가져오기
  let apiUrl = '/api/disease';
  if (countryQuery) {
    apiUrl += `?country=${encodeURIComponent(countryQuery)}`;
  }
  console.log(`질병 발생 데이터 로딩 중... URL: ${apiUrl}`);

  try {
    // getDiseaseData()는 URL 파라미터를 받지 않으므로, 직접 fetch 또는 apiHandler 수정 필요
    // 여기서는 getDiseaseData()가 필터 없는 전체 데이터를 가져온다고 가정
    const events = await getDiseaseData(); // apiHandler.js의 함수 호출

    if (events.error) { 
      alert(`질병 정보 오류: ${events.error}`); 
      console.error("질병 정보 로드 오류:", events.error);
      return; 
    }
    if (!Array.isArray(events)) { 
      alert("질병 정보 데이터 형식이 잘못되었습니다 (배열이 아님)."); 
      console.error("질병 정보 데이터 형식이 배열이 아님:", events);
      return;
    }

    let displayedCount = 0;
    events.forEach(event => {
        if (!event.latitude || !event.longitude) { // DB에서 직접 컬럼 사용
            return;
        }
        displayedCount++;
        const icon = disasterIcons['Disease Outbreak'];
        const marker = L.circleMarker([event.latitude, event.longitude], {
            radius: 6, fillColor: '#8A2BE2', color: '#FFF', weight: 1, fillOpacity: 0.7,
        }).addTo(map);
        const safeTitle = event.title?.replace(/</g, "<") || "제목 없음";
        const safeDesc = event.description?.replace(/</g, "<")?.substring(0,200) || "설명 없음";
        marker.bindPopup(`<h4>${icon} ${safeTitle}</h4><p>📅 ${new Date(event.date).toLocaleDateString('ko-KR')}</p><p>🌍 국가: ${event.country || 'N/A'}</p><p>📄 내용: ${safeDesc}...</p>${event.link ? `<p><a href="${event.link}" target="_blank">상세보기</a></p>`:''}<p><em>출처: ${event.source_data || '정보 없음'}</em></p>`);
        diseaseMarkers.push(marker);
    });
    console.log(`질병 발생 정보 ${displayedCount}개 표시 완료. (총 ${events.length}개 수신)`);
  } catch (error) {
      console.error("질병 정보 요청/처리 중 오류:", error);
      alert("질병 정보를 가져오는 중 오류가 발생했습니다.");
  }
}


// --- 지도 클릭 이벤트 (날씨 정보) ---
map.on('click', async function(e) {
  const { lat, lng } = e.latlng;
  console.log(`지도 클릭: 위도=${lat}, 경도=${lng}`); 

  const weatherInfo = await fetchWeather(lat, lng); 
  console.log("날씨 정보 응답:", weatherInfo); 

  if (weatherInfo.error) {
    console.error("날씨 정보 가져오기 오류 (main.js):", weatherInfo.error);
    L.popup()
     .setLatLng(e.latlng)
     .setContent(`<p>날씨 정보를 가져올 수 없습니다.<br>${weatherInfo.error}</p>`) 
     .openOn(map);
    return;
  }

  const weatherIconUrl = `https://openweathermap.org/img/wn/${weatherInfo.icon}@2x.png`;
  const weatherPopupContent = `
    <h4>${weatherInfo.location || "선택 위치"} 날씨</h4>
    <p><img src="${weatherIconUrl}" alt="${weatherInfo.weather}" style="vertical-align: middle; width: 50px; height: 50px;"> ${weatherInfo.weather}</p>
    <p><strong>🌡️ 온도:</strong> ${weatherInfo.temperature}°C</p>
    <p><strong>💧 습도:</strong> ${weatherInfo.humidity}%</p>
    <p><strong>💨 풍속:</strong> ${weatherInfo.wind_speed} m/s</p>
  `;

  L.popup()
    .setLatLng(e.latlng)
    .setContent(weatherPopupContent)
    .openOn(map);
});

// --- DOM 로드 후 초기화 ---
document.addEventListener("DOMContentLoaded", () => {
  const controlPanelToggleBtn = document.getElementById('control-panel-toggle-btn');
  const controlPanelWrapper = document.querySelector('.control-panel-wrapper');
  const closeControlPanelBtn = document.getElementById('close-control-panel-btn');

  if (controlPanelToggleBtn && controlPanelWrapper) {
    controlPanelToggleBtn.addEventListener('click', () => {
      controlPanelWrapper.classList.toggle('show');
    });
  }
  if (closeControlPanelBtn && controlPanelWrapper) {
    closeControlPanelBtn.addEventListener('click', () => {
      controlPanelWrapper.classList.remove('show');
    });
  }

  document.getElementById('year-filter')?.addEventListener('change', loadAndDisplayEonet);
  document.getElementById('category-filter')?.addEventListener('change', loadAndDisplayEonet);

  document.getElementById('toggle-eonet')?.addEventListener('change', loadAndDisplayEonet);
  document.getElementById('toggle-gdacs')?.addEventListener('change', loadAndDisplayGdacs); 
  document.getElementById('toggle-disease')?.addEventListener('change', loadAndDisplayDisease); 

  if (document.getElementById('toggle-gdacs')?.checked) loadAndDisplayGdacs(); 
  if (document.getElementById('toggle-disease')?.checked) loadAndDisplayDisease(); 
});