import { WeatherCondition } from '../components/WeatherIcon';

export interface WeatherData {
  temperature: number;
  windSpeed: number;
  windDirection: number; // In degrees: 0 = N, 90 = E, 180 = S, 270 = W
  pressure: number;
  condition: WeatherCondition;
  waveHeight: number;
  rainfall: number;
  tsunamiRisk: boolean;
  floodRisk: boolean;
  batteryLevel: number;
  signalStrength: number;
  lastUpdate: string;
  waterTemperature: number;
  waveHistory: { time: string, height: number }[];
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// This function will either fetch real data or return mock data based on environment
export async function fetchWeatherData(): Promise<WeatherData | null> {  
  try {
    if (!API_URL) {
      throw new Error('API_URL is not defined. Please check your environment variables.');
    }

    const response = await fetch(`${API_URL}/api/weather`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} - ${response.statusText}`);
    }

    const data: WeatherData = await response.json();

    // Validate the response structure (optional, but recommended)
    if (!data || typeof data.temperature !== 'number') {
      throw new Error('Invalid API response structure.');
    }

    return data;
  } catch (error) {
    console.error('Failed to fetch weather data:', error);
    return null; // Return null to indicate failure
  }
}
