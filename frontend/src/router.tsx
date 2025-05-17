import { HashRouter, Route, Routes } from 'react-router-dom';
import App from './App';
import About from './About';

const router = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </HashRouter>
  );
};

export default router;
