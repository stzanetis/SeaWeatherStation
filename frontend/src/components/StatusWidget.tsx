import { Sun } from 'lucide-react';

const StatusWidget = () => {
    return (
        <div className="bg-foreground text-text font-bold p-3 rounded-[12px] shadow-lg w-full h-40">
            <h2 className="text-[16px] text-text font-sansation font-bold">Drone Status</h2>
            <div className="mt-4 space-y-4">
                <div>
                    <div className="flex justify-between text-[14px] mb-1">
                        <span className="text-text-secondary font-semibold">Battery</span>
                        <span className="text-text-accent">75%</span>
                    </div>
                    <div className="w-full bg-gray-300 rounded-full h-2.5">
                        <div className="bg-text h-2.5 rounded-full" style={{ width: '75%' }}></div>
                    </div>
                </div>
                <div>
                    <div className="flex justify-between text-[14px] mb-1">
                        <span className="text-text-secondary font-semibold">Signal Strength</span>
                        <span className="text-text-accent">60%</span>
                    </div>
                    <div className="w-full bg-gray-300 rounded-full h-2.5">
                        <div className="bg-text h-2.5 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default StatusWidget;