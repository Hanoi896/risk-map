// static/js/apiHandler.js

async function fetchData(endpoint, dataName) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        const errorText = await response.text();
        console.error(`${dataName} API 오류 응답 (텍스트): ${response.status} - ${errorText}`);
        return { error: `${dataName} API 오류 (${response.status}): ${errorText || response.statusText}` };
      }
      console.error(`${dataName} API 오류 응답 (JSON): ${response.status}`, errorData);
      return { error: errorData.error || `${dataName} API 오류 (${response.status})` };
    }
    const data = await response.json();
    if (!Array.isArray(data)) {
      console.error(`${dataName} API가 배열을 반환하지 않았습니다 (오류 객체도 아님):`, data);
      return { error: `${dataName} 데이터 형식이 올바르지 않습니다. (배열이 아님)` };
    }
    return data;
  } catch (error) {
    console.error(`${dataName} 데이터를 가져오는 중 클라이언트 네트워크/fetch 오류 발생:`, error);
    return { error: error.message || `${dataName} 데이터를 가져오는데 실패했습니다. (네트워크 오류)` };
  }
}

export async function fetchWeather(lat, lon) {
  try {
    const response = await fetch(`/api/weather?lat=${lat}&lon=${lon}`);
    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        const errorText = await response.text();
        console.error(`날씨 API 오류 응답 (텍스트): ${response.status} - ${errorText}`);
        return { error: `날씨 API 오류 (${response.status}): ${errorText || response.statusText}` };
      }
      console.error(`날씨 API 오류 응답 (JSON): ${response.status}`, errorData);
      return { error: errorData.error || `날씨 API 오류 (${response.status})` };
    }
    return await response.json();
  } catch (error) {
    console.error("날씨 데이터를 가져오는 중 클라이언트 네트워크/fetch 오류 발생:", error);
    return { error: error.message || "날씨 정보를 가져오는 데 실패했습니다. (네트워크 오류)" };
  }
}

export async function getEonetData() {
  return fetchData('/api/eonet', 'EONET');
}

export async function getGdacsData() {
  return fetchData('/api/gdacs', 'GDACS');
}

export async function getDiseaseData() {
  return fetchData('/api/disease', '질병 발생 정보');
}

// ACLED 함수 제거
// export async function getAcledData() {
//   return fetchData('/api/acled', 'ACLED 분쟁 정보');
// }