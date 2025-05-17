import React from 'react'
import ReactDOM from 'react-dom/client'
import Router from './router' // Import your router component
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>,
)
