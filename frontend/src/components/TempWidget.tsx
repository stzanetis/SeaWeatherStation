import { Thermometer } from 'lucide-react';
import { getInfo } from '@/services/api';
import { useEffect, useState } from 'react';

const TempWidget = () => {
    const [temperature, setTemperature] = useState(null);
    const [temperatureDescription, setTemperatureDescription] = useState(null);

    const fetchTemperature = async () => {
        try {
            const infoData = await getInfo();
            setTemperature(infoData.temperature);

            if (infoData.temperature < 10) {
                setTemperatureDescription('Cold');
            } else if (infoData.temperature >= 10 && infoData.temperature < 20) {
                setTemperatureDescription('Mild');
            } else if (infoData.temperature >= 20 && infoData.temperature < 30) {
                setTemperatureDescription('Warm');
            } else {
                setTemperatureDescription('Hot');
            }
        } catch (error) {
            console.error('Error fetching temperature data:', error);
        }
    };

    useEffect(() => {
        fetchTemperature();

        // Set up an interval to fetch data every 30s
        const intervalId = setInterval(fetchTemperature, 30000);
        
        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="transition-transform active:scale-95 bg-foreground/60 border-l border-t border-white/60 backdrop-blur-sm p-3 p-3 rounded-[12px] shadow-lg w-full h-44">
            <h2 className="text-[16px] text-text font-sansation font-bold">Air Temperature</h2>
            {temperature !== null && (
                <div>
                    <div className="mt-4 mb-2">
                        <Thermometer className="text-text" strokeWidth={2} size={50} />
                    </div>
                    <h1 className="text-[32px] text-text-accent font-sansation font-bold">{temperature}°C</h1>
                    <h3 className="text-[11px] text-text-secondary font-sansation">{temperatureDescription}</h3>
                </div>
            )}
        </div>
    );
}

export default TempWidget;