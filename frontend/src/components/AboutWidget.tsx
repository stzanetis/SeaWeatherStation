import { Ghost } from "lucide-react"
import { useNavigate } from "react-router-dom" 

const AboutWidget = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        // Play a click sound if desired
        // const audio = new Audio('/assets/click.mp3');
        // audio.play().catch(err => console.error('Error playing sound:', err));
        
        // Navigate to the About page
        setTimeout(() => {
            navigate('/about');
        }, 300);
    };

    return (
        <div 
            onClick={handleClick}
            className="transition-transform active:scale-95 bg-foreground/60 border-l border-t border-white/60 backdrop-blur-sm p-3 rounded-[12px] shadow-lg w-full h-36"
        >
            <h2 className="text-[16px] text-text font-sansation font-bold">About the project</h2>
            <Ghost className="text-text mt-3 mb-3" strokeWidth={2} size={50} />
            <p className="text-[12px] text-text-secondary font-sansation">Click to learn more</p>
        </div>
    );
}

export default AboutWidget;
