import { getWave } from '@/services/api';
import { useEffect, useState } from 'react';

const ShoreWidget = () => {
    const [inundation, setInundation] = useState(null);
    const [inundationDescription, setInundationDescription] = useState(null);

    const fetchPressure = async () => {
        try {
            const waveData = await getWave();
            const currentInundation = waveData.inundation;
            setInundation(currentInundation);

            if (currentInundation < 2) {
                setInundationDescription('Below average');
            } else if (currentInundation >= 2 && currentInundation <= 5) {
                setInundationDescription('Average');
            } else {
                setInundationDescription('Above average');
            }

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        fetchPressure();

        // Set up an interval to fetch data every 30s
        const intervalId = setInterval(fetchPressure, 30000);
        
        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="w-full transition-transform active:scale-95 bg-foreground/60 border-l border-t border-white/60 backdrop-blur-sm p-3 rounded-[12px] shadow-lg w-44 h-36">
            <h2 className="text-[16px] text-text font-sansation font-bold">Avg Dist to Shore</h2>
            {inundation !== null && (
                <div>
                    <div className="grid"></div>
                    <div className="flex flex-col justify-center h-[calc(100%-50px)] mt-3.5">
                        <h1 className="text-[32px] text-text-accent font-sansation font-bold">{inundation}</h1>
                        <h3 className="text-[11px] text-text font-bold font-sansation">Meters</h3>
                        <h3 className="text-[11px] text-text-secondary font-sansation mt-2">{inundationDescription}</h3>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ShoreWidget;