import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './Dashboard';  // Correct import
import Insights from './Insights';    // Correct import
import './Dashboard.module.css';      // Include any CSS styling here
import './Insights.module.css';       // Include any CSS styling here

function App() {
  return (
    <Router>
      
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/insights" element={<Insights />} />
        </Routes>
    
    </Router>
  );
}

export default App;
