import React, { useEffect, useState } from 'react';
import './components/styles/App.scss';

import useSocket from './hooks/useSocket';

import CameraWidget from './components/CameraWidget';
import WeatherWidget from './components/WeatherWidget';
// import PiholeWidget from './components/PiholeWidget';
import PiSystemWidget from './components/PiSystemWidget';
import NetworkWidget from './components/NetworkWidget';


function App() {

  const {socket, socketOpen} = useSocket();
  const [climateData, setClimateData] = useState(null);
  const [systemData, setSystemData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  // const [networkData, setNetworkData] = useState(null);

  useEffect(() => {
    if (socketOpen) {
      console.log('listening');
      socket.onmessage = msg => {
        // console.log(msg);
        const data = JSON.parse(msg.data);
        // console.log(data);
        if (data.timestamp) {
          setClimateData(data.climateData);
          setSystemData(data.systemData);
          setLastUpdated(data.timestamp);
        } else {
          console.log('Error: difficulty getting data');
          socket.send("well gawd damn");
        }
        
      };
    }
  }, [socket, socketOpen]);


  return (
    <div className="app">
      <header>Inclement-Pi</header>
      <p>Last Updated: {lastUpdated}</p>
      <div className="widget-container">
        <div className="widget-subdivide-1">
          <WeatherWidget climateData={climateData} ></WeatherWidget>
          <PiSystemWidget systemData={systemData} ></PiSystemWidget>
          <NetworkWidget></NetworkWidget>
        </div>
        <div className="widget-subdivide-2">
          <CameraWidget></CameraWidget>
        </div>
      </div>
    </div>
  );
}

export default App;
