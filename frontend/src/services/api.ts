export const API_BASE_URL = 'http://192.168.1.3:5000/';

// Helper function for making API requests
async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    signal: controller.signal,
  });

  clearTimeout(timeoutId);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `API error: ${response.status}`);
  }

  return response.json();
}

// Check status
export const checkStatus = async () => {
  try {
    const response = await fetchAPI('status');
    return response;
  } catch (error) {
    return false;
  }
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
