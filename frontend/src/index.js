import React from 'react';
import ReactDOM from 'react-dom/client'; // Make sure you're importing from 'react-dom/client'
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root')); // Get the root div
root.render(<App />); // Use createRoot to render the app
