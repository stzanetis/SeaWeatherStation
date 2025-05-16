import {useState, useEffect} from 'react';
import { checkStatus } from '@/services/api';

const StatusWidget = () => {
    const [battery, setBattery] = useState(null);
    const [signal, setSignal] = useState(null);

    const fetchStatus = async () => {
        try {
            const statusData = await checkStatus();

            if (!statusData) {
                return;
            }
            setBattery(statusData.battery);
            setSignal(statusData.signal_strength);
        } catch (error) {
            console.error('Error fetching status data:', error);
        }
    };

    useEffect(() => {
        fetchStatus();

        // Set up an interval to fetch status data every 30s
        const intervalId = setInterval(fetchStatus, 30000);

        // Clean up the interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="bg-foreground p-3 rounded-[12px] shadow-lg w-full h-40">
            <h2 className="text-[16px] text-text font-sansation font-bold">Drone Status</h2>
            {battery !== null && signal !== null && (
                <div className="mt-4 space-y-4">
                    <div>
                        <div className="flex justify-between text-[14px] mb-1">
                            <span className="text-text-secondary font-semibold font-sansation">Battery</span>
                            <span className="text-text-accent font-semibold font-sansation">{battery}%</span>
                        </div>
                        <div className="w-full bg-gray-300 rounded-full h-2">
                            <div className={`h-2 rounded-full ${battery < 25 ? 'bg-warning_high-border' : 'bg-text'}`} style={{ width: `${battery}%` }}></div>
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between text-[14px] mb-1">
                            <span className="text-text-secondary font-semibold font-sansation">Signal Strength</span>
                            <span className="text-text-accent font-semibold font-sansation">{signal}%</span>
                        </div>
                        <div className="w-full bg-gray-300 rounded-full h-2">
                            <div className={`h-2 rounded-full ${signal < 50 ? 'bg-warning_high-border' : 'bg-text'}`} style={{ width: `${signal}%` }}></div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default StatusWidget;