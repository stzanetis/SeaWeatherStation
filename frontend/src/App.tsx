import background from '@/assets/background.jpg';
import { checkStatus } from '@/services/api';
import { useEffect } from 'react';
import { MapPin } from 'lucide-react';

import WeatherWidget from '@/components/CondWidget';
import TempWidget from '@/components/TempWidget';
import PressWidget from '@/components/PressWidget';
import WindWidget from '@/components/WindWidget';
import StatusWidget from '@/components/StatusWidget';
import WaveWidget from '@/components/WaveWidget';

const App = () => {

  useEffect(() => {
    async function fetchStatus() {
      const status = await checkStatus();
      if (status.online === true) {
      } else {
      }
    }
    fetchStatus();
  }, []);

  return (
    <div
      className="min-h-screen p-4 md:p-8 w-full relative inset-0 bg-cover bg-center"
      style={{
        backgroundImage: `linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 77, 180, 100)), url(${background})`
      }}
    >
      <div className="max-w-7xl mt-10 mx-auto">
        <h1 className="text-text text-[2.4rem] font-sansation tracking-tight ml-3 pb-2 font-bold">Sea Weather Station</h1>
        
        <div className="mt-6">
          <div className="flex items-center font-bold">
            <MapPin className="text-text-accent text-[4rem]" strokeWidth={2.5} />
            <h2 className="text-text-accent font-sansation text-[1.1rem] ml-1">Thessaloniki, Greece</h2>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
            <WeatherWidget />
            <TempWidget />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-3.5">
            <StatusWidget />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
            <PressWidget />
            <WindWidget />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-3.5">
            <WaveWidget />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App;
