import React, { useEffect, useState } from 'react';
import './App.css';

import useSocket from './hooks/useSocket';

import NetworkWidget from './components/NetworkWidget';


function App() {

  const {socket, socketOpen} = useSocket();
  const [climateData, setClimateData] = useState(null);
  const [networkData, setNetworkData] = useState(null);

  useEffect(() => {
    if (socketOpen) {
      console.log('listening');
      socket.onmessage = msg => {
        const data = JSON.parse(msg.data);
        if (data.climate_data) {
          setClimateData(data.climate_data);
          setNetworkData(data.network_data);
          console.log('fuuuuuck');
        } else {
          console.log('Error: difficulty getting data');
        }
        
      };
    }
  }, [socket, socketOpen]);


  return (
    <div className="App">
      <header>Inclement-Pi</header>
      <NetworkWidget networkData={networkData} ></NetworkWidget>
    </div>
  );
}

export default App;