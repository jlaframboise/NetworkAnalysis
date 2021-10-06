import React, { useState, useEffect } from 'react';
import './App.css';

import Dashboard from './components/Dashboard.js';


/*
A functional react component to render our app by
calling on the Dashboard component. 
*/
function App() {

  // We use the current time to check that we are 
  // connected to the backend api. 
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  // return our dashboard functional component
  return (
    Dashboard()
  );
}

export default App;
