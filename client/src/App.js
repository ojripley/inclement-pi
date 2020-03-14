import React, { useEffect, useState } from 'react';
import './App.css';

import useSocket from './hooks/useSocket';

import NetworkWidget from './components/NetworkWidget';
import WeatherWidget from './components/WeatherWidget';


function App() {

  const {socket, socketOpen} = useSocket();
  const [climateData, setClimateData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  // const [networkData, setNetworkData] = useState(null);

  useEffect(() => {
    if (socketOpen) {
      console.log('listening');
      socket.onmessage = msg => {
        console.log(msg);
        const data = JSON.parse(msg.data);
        console.log(data);
        if (data.timestamp) {
          setClimateData(data.climateData);
          setLastUpdated(timestamp);
        } else {
          console.log('Error: difficulty getting data');
        }
        
      };
    }
  }, [socket, socketOpen]);


  return (
    <div className="App">
      <header>Inclement-Pi</header>
      {/* <NetworkWidget networkData={networkData} ></NetworkWidget> */}
      <WeatherWidget climateData={climateData}></WeatherWidget>
      <p>Last Updated: {lastUpdated}</p>
    </div>
  );
}

export default App;
