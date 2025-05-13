import { Sun, Cloudy, CloudRainWind } from 'lucide-react';
import { getWeather } from '@/services/api';
import { useEffect, useState } from 'react';

const WeatherWidget = () => {
    const [weather, setWeather] = useState(null);
    const [weatherIcon, setWeatherIcon] = useState(null);
    const [weatherDescription, setWeatherDescription] = useState(null);

    const fetchWeather = async () => {
        try {
            const weatherData = await getWeather();
            setWeather(weatherData.condition);
            setWeatherDescription(
                weatherData.description.charAt(0).toUpperCase() + 
                weatherData.description.slice(1)
            );
            if (weatherData.condition === 'Clear') {
                setWeatherIcon(<Sun className="text-text text-yellow-700" strokeWidth={2} size={50} />);
            } else if (weatherData.condition === 'Rain') {
                setWeatherIcon(<CloudRainWind className="text-text text-gray-700" strokeWidth={2} size={50} />);
            } else if (weatherData.condition === 'Clouds') {
                setWeatherIcon(<Cloudy className="text-text" strokeWidth={2} size={50} />);
            }
        } catch (error) {
            console.error('Error fetching weather data:', error);
        }
    };

    useEffect(() => {
        // Fetch immediately when component mounts
        fetchWeather();

        // Set up an interval to fetch weather data every minute
        const intervalId = setInterval(fetchWeather, 60000);
        
        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="bg-foreground p-3 rounded-[12px] shadow-lg w-44 h-44">
            <h2 className="text-[16px] text-text font-sansation font-bold">Current Condition</h2>
            <div className="mt-4 mb-2">
                {weatherIcon}
            </div>
            <h1 className="text-[32px] text-text-accent font-sansation font-bold">{weather}</h1>
            <h3 className="text-[11px] text-text-secondary font-sansation">{weatherDescription}</h3>
        </div>
    );
}

export default WeatherWidget;