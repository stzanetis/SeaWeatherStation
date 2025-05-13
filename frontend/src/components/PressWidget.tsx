import { getInfo } from '@/services/api';
import { useEffect, useState } from 'react';

const PressWidget = () => {
    const [pressure, setPressure] = useState(null);
    const [pressureDescription, setPressureDescription] = useState(null);

    const fetchPressure = async () => {
        try {
            const infoData = await getInfo();
            setPressure(infoData.pressure);

            if (infoData.pressure < 1000) {
                setPressureDescription('Below average');
            } else if (infoData.pressure >= 1000 && infoData.pressure <= 1020) {
                setPressureDescription('Normal Pressure');
            } else {
                setPressureDescription('Above average');
            }
        } catch (error) {
            console.error('Error fetching pressure data:', error);
        }
    };

    useEffect(() => {
        fetchPressure();

        // Set up an interval to fetch weather data every minute
        const intervalId = setInterval(fetchPressure, 60000);
        
        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="bg-foreground p-3 rounded-[12px] shadow-lg w-44 h-36">
            <h2 className="text-[16px] text-text font-sansation font-bold">Pressure</h2>
            <div className="grid"></div>
            <div className="flex flex-col justify-center h-[calc(100%-50px)] mt-3.5">
                <h1 className="text-[32px] text-text-accent font-sansation font-bold">{pressure}</h1>
                <h3 className="text-[11px] text-text font-bold font-sansation">hPa</h3>
                <h3 className="text-[11px] text-text-secondary font-sansation mt-2">{pressureDescription}</h3>
            </div>
            
        </div>
    );
}

export default PressWidget;