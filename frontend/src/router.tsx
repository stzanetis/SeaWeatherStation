import { HashRouter, Route, Routes } from 'react-router-dom';
import App from './App';
import About from './About';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: '/about',
    element: <About />
  }
], {
  basename: '/SeaWeatherStation'
});

export default router;
