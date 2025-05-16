import { motion, AnimatePresence } from 'framer-motion';
import background from '@/assets/background.svg';
import { checkStatus } from '@/services/api';
import { useEffect, useState } from 'react';
import { MapPin } from 'lucide-react';

import WeatherWidget from '@/components/CondWidget';
import TempWidget from '@/components/TempWidget';
import PressWidget from '@/components/PressWidget';
import WindWidget from '@/components/WindWidget';
import StatusWidget from '@/components/StatusWidget';
import WaveWidget from '@/components/WaveWidget';
import AboutWidget from '@/components/AboutWidget';
import AlertWidget from '@/components/AlertWidget';

const App = () => {
  const [showConnectionAlert, setShowConnectionAlert] = useState(false);
  const [showTsunamiAlert, setShowTsunamiAlert] = useState(false);

  const fetchStatus = async () => {
    try {
      const statusData = await checkStatus();
      if (!statusData) {
        setShowConnectionAlert(true);
      } else {
        setShowConnectionAlert(false);
      }
    } catch (error) {
      console.error('Error fetching status data:', error);
      setShowConnectionAlert(true);
    }
  };

  useEffect(() => {
    fetchStatus();

    // Set up an interval to fetch status data every 30s
    const intervalId = setInterval(fetchStatus, 30000);

    // Clean up the interval when component unmounts
    return () => clearInterval(intervalId);
  }, []);

  const handleConnectionAlertClose = () => {
    setShowConnectionAlert(false);
  };

  const handleTsunamiAlertClose = () => {
    setShowTsunamiAlert(false);
  };

  return (
    <main
      className="min-h-screen p-4 w-full bg-cover bg-center"
      style={{backgroundImage: `url(${background})`}}>
      <div className="mt-10 mx-auto">

        {/* Title */}
        <h1 className="text-text text-[2.4rem] font-sansation tracking-tight pb-2 font-bold">Sea Weather Station</h1>
        
        {/* Location */}
        <div className="flex items-center font-bold mt-6">
          <MapPin className="text-text-accent text-[4rem]" strokeWidth={2.5} />
          <h2 className="text-text-accent font-sansation text-[1.1rem] ml-1">Thessaloniki, Greece</h2>
        </div>
          
        {/* Connection Alert */}
        <AnimatePresence> {showConnectionAlert && (
          <motion.div
            initial={{ height: 0, opacity: 0, marginBottom: 0 }}
            animate={{ height: 'auto', opacity: 1, marginBottom: 16 }}
            exit={{ height: 0, opacity: 0, marginBottom: 0 }}
            transition={{ duration: 0.3 }}
            className="mt-4"
          >
            <AlertWidget 
              onClose={handleConnectionAlertClose}
              title="Connection Error"
              severity='low'
              description="The weather station is currently offline. Please check your connection."
            />
           </motion.div>
        )} </AnimatePresence>
        
        {/* Tsunami Alert */}
        <AnimatePresence> {showTsunamiAlert && (
          <motion.div
            initial={{ height: 0, opacity: 0, marginBottom: 0 }}
            animate={{ height: 'auto', opacity: 1, marginBottom: 16 }}
            exit={{ height: 0, opacity: 0, marginBottom: 0 }}
            transition={{ duration: 0.3 }}
            className="mt-4"
          >
            <AlertWidget 
              onClose={handleTsunamiAlertClose}
              title="Tsunami Warning"
              severity='high'
              description="A tsunami warning has been issued for the area. Please evacuate immediately."
            />
          </motion.div>
        )} </AnimatePresence>
        
        {/* Widgets */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          <WeatherWidget />
          <TempWidget />
        </div>

        <div className="mr-[-2px] mt-4">
          <WaveWidget />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <PressWidget />
          <WindWidget />
        </div>

        <div className="mr-[-2px] mt-4">
          <StatusWidget />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <AboutWidget />
        </div>

        <br />
      </div>
    </main>
  )
}

export default App;
