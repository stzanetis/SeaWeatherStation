import { useState, useEffect, use } from 'react';
import { BadgeAlert, X } from 'lucide-react';
import { motion } from 'framer-motion';
import { text } from 'stream/consumers';

interface AlertWidgetProps {
    onClose: () => void;
    severity: 'low' | 'high';
    description: string;
    title: string;
}

const AlertWidget = ({onClose, description, title, severity}: AlertWidgetProps) => {
    const [isVisible, setIsVisible] = useState(true);
    const [showContent, setShowContent] = useState(false);
    const [colors, setColors] = useState({
        background: 'bg-warning_low',
        border: 'border-warning_low-border',
        text: 'text-text-warning_low',
    });

    const handleClose = () => {
        setShowContent(false);
        
        setTimeout(() => {
            setIsVisible(false);
            setTimeout(() => {
                onClose();
            }, 300);
        }, 150);
    };

    useEffect(() => {
        if (severity === 'low') {
            setColors({
                background: 'bg-warning_low',
                border: 'border-warning_low-border',
                text: 'text-text-warning_low',
            });
        } else if (severity === 'high') {
            setColors({
                background: 'bg-warning_high',
                border: 'border-warning_high-border',
                text: 'text-text-warning_high',
            });
        }
    }, []);
    
    useEffect(() => {
        setIsVisible(true);
    }, []);
    
    useEffect(() => {
        if (isVisible) {
            const timer = setTimeout(() => {
                setShowContent(true);
            }, 300);
            return () => clearTimeout(timer);
        } else {
            setShowContent(false);
        }
    }, [isVisible]);

    return (
        <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: isVisible ? 1 : 0, height: isVisible ? 'auto' : 0 }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className={`${colors.background} ${colors.border} ${colors.text} transition-transform active:scale-95 border-2 p-3 rounded-[12px] shadow-lg w-full`}
        >
            <div className="flex justify-between items-center">
                <h2 className="text-[18px] font-sansation font-bold flex items-center">
                    <BadgeAlert className="mr-2" size={24} />
                    {title}
                </h2>
                <button 
                    onClick={handleClose}
                    className="bg-white/0 p-1 transition-colors outline-none focus:outline-none focus:ring-0">
                    <X size={20} />
                </button>
            </div>
            <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: showContent ? 1 : 0 }}
                transition={{ duration: 0.15 }}
                className="mt-2"
            >
                {description}
            </motion.p>
        </motion.div>
    );
}

export default AlertWidget;