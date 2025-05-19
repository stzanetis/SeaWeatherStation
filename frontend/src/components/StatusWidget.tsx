import {useState, useEffect} from 'react';
import { checkStatus } from '@/services/api';

const StatusWidget = () => {
    const [battery, setBattery] = useState(null);
    const [signal, setSignal] = useState(null);
    const [signalLevel, setSignalLevel] = useState(0);

    const fetchStatus = async () => {
        try {
            const statusData = await checkStatus();

            if (!statusData) {
                return;
            }
            setBattery(statusData.battery);

            // Convert signal strength from dBm to linear percentage
            // For RF22 Module: -40  dBm = 100% signal strength
            //                  -120 dBm = 0%   signal strength
            let signalLevel = 1.25 * statusData.signal_strength + 150;
            signalLevel = Math.max(0, Math.min(100, signalLevel));
            signalLevel = Math.round(signalLevel);

            setSignal(statusData.signal_strength);
            setSignalLevel(signalLevel);
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
        <div className="transition-transform active:scale-95 bg-foreground/60 border-l border-t border-white/60 backdrop-blur-sm p-3 rounded-[12px] shadow-lg w-full h-40">
            <h2 className="text-[16px] text-text font-sansation font-bold">Drone Status</h2>
            {battery !== null && signal !== null && (
                <div className="mt-4 space-y-4">
                    <div>
                        <div className="flex justify-between text-[14px] mb-1">
                            <span className="text-text-secondary font-semibold font-sansation">Battery</span>
                            <span className="text-text-accent font-semibold font-sansation">{battery}%</span>
                        </div>
                        <div className="w-full bg-white/60 rounded-full h-2">
                            <div 
                                className="h-2 rounded-full" 
                                style={{ 
                                    width: `${battery}%`,
                                    background: battery < 25 ? 'linear-gradient(90deg, #9c1717, #cf2727)' :
                                                battery < 50 ? 'linear-gradient(90deg, #ad7400, #d68f00)' :
                                                'linear-gradient(90deg, #00174a, #002b88)'}}
                            ></div>
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between text-[14px] mb-1">
                            <span className="text-text-secondary font-semibold font-sansation">Signal Strength</span>
                            <span className="text-text-accent font-semibold font-sansation">{signalLevel}% ({signal} dBm)</span>
                        </div>
                        <div className="w-full bg-white/60 rounded-full h-2">
                            <div 
                                className={"h-2 rounded-full"} 
                                style={{ 
                                    width: `${signalLevel}%` ,
                                    background: signalLevel < 25 ? 'linear-gradient(90deg, #9c1717, #cf2727)' :
                                                signalLevel < 50 ? 'linear-gradient(90deg, #ad7400, #d68f00)' :
                                                'linear-gradient(90deg, #00174a, #002b88'}}
                            ></div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default StatusWidget;