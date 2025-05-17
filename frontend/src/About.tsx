import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import background from '@/assets/background.svg';

const About = () => {
    const navigate = useNavigate();
    
    return (
        <div className="min-h-screen p-4 text-text bg-cover bg-center" style={{backgroundImage: `url(${background})`}}>
            <div className="flex justify-between items-center mb-6 mt-6">
                <div className="flex flex-col items-start">
                    <h2 className="text-2xl font-bungee">About</h2>
                    <h1 className="text-4xl font-bungee">S.W.E.L.L</h1>
                </div>
                
                <button 
                    onClick={() => {
                        setTimeout(() => {
                            navigate('/')
                        }, 300)
                    }}
                    className="bg-foreground/60 
                    backdrop-blur-sm flex items-center text-text shadow-lg 
                    border-l border-t border-white/60 font-sansation font-bold"
                >
                    <ArrowLeft className="mr-2" size={20} />
                    Back
                </button>
            </div>
            
            <div className="bg-foreground/60 backdrop-blur-sm p-6 rounded-[12px] shadow-lg border-l border-t border-white/60">
                <h2 className="text-2xl font-sansation font-bold mb-4">Sea-level Weather Estimation and Live Logging</h2>
                
                <p className="mb-4 text-text-secondary">
                    S.W.E.L.L is an advanced maritime monitoring system designed to track and analyze 
                    sea conditions, weather patterns, and coastal phenomena in real-time.
                </p>
                
                <h3 className="text-xl font-sansation font-bold mt-6 mb-2">Features</h3>
                <ul className="list-disc pl-5 text-text-secondary">
                    <li>Real-time wave height and pattern monitoring</li>
                    <li>Temperature and pressure tracking</li>
                    <li>Wind speed and direction analysis</li>
                    <li>Coastal inundation and flood risk assessment</li>
                    <li>Early warning system for extreme weather events</li>
                </ul>
                
                <h3 className="text-xl font-sansation font-bold mt-6 mb-2">Who we are</h3>
                <ul className="list-disc pl-5 text-text-secondary">
                    <li>Iasonas Lamprinidis</li>
                    <li>Ioannis Michalainas</li>
                    <li>Savvas Tzanetis</li>
                    <li>Vasileios Zoidis</li>
                </ul>
                
                <h3 className="text-xl font-sansation font-bold mt-6 mb-2">Git-Hub Page</h3>
                <p className="text-text-secondary">
                    The entire project is open-source and available on GitHub. You can find the code as well as any documentation 
                    at <a href="https://github.com/ioannisam/SeaWeatherStation" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">github.com/ioannisam/SeaWeatherStation</a>.
                </p>
            </div>
            <br />
        </div>
    );
}

export default About;