import React, { useEffect, useState } from 'react';
import './App.css';

import useSocket from './hooks/useSocket';

import NetworkWidget from './components/NetworkWidget';
import WeatherWidget from './components/WeatherWidget';
import PiholeWidget from './components/PiholeWidget';
import PiSystemWidget from './components/PiSystemWidget';


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
    <div className="App">
      <header>Inclement-Pi</header>
      {/* <NetworkWidget networkData={networkData} ></NetworkWidget> */}
      <PiholeWidget></PiholeWidget>
      <WeatherWidget climateData={climateData} ></WeatherWidget>
      <PiSystemWidget systemData={systemData} ></PiSystemWidget>
      <p>Last Updated: {lastUpdated}</p>
    </div>
  );
}

export default App;
