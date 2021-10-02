import React, { useState, useEffect } from 'react';
import { ReactDOM } from 'react';
import logo from './logo.svg';
import './App.css';

import Button from '@mui/material/Button';

import Dashboard from './components/Dashboard.js';

function App() {

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    Dashboard()
    // <div className="App">
    //   <header className="App-header">
        
    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>
    //       Edit <code>src/App.js</code> and save to reload.
    //     </p>
    //     <a
    //       className="App-link"
    //       href="https://reactjs.org"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       Learn React
    //     </a>
    //     <p>The current time is {currentTime}</p>
    //     <Button variant="contained">Hello world from Material UI!</Button>
    //   </header>
    // </div>
  );
}

export default App;
