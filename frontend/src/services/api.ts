export const API_BASE_URL = 'http://192.168.1.10:5000/';

// Helper function for making API requests
async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `API error: ${response.status}`);
  }

  return response.json();
}

// Check status
export const checkStatus = async () => {
  const response = await fetchAPI('status');
  return response;
};

// Get temperature and pressure data
export const getInfo = async () => {
  const infoData = await fetchAPI('info');
  return infoData;
};

// Get weather and wind data
export const getWeather = async () => {
  const weatherData = await fetchAPI('weather');
  return weatherData;
};
