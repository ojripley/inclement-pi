import React, { useEffect, useState } from 'react';
import './components/styles/App.scss';

import useSocket from './hooks/useSocket';
import useCommandSocket from './hooks/useCommandSocket';

import TitleWidget from './components/TitleWidget';
import CameraWidget from './components/CameraWidget';
import WeatherWidget from './components/WeatherWidget';
// import PiholeWidget from './components/PiholeWidget';
import PiSystemWidget from './components/PiSystemWidget';
import NetworkWidget from './components/NetworkWidget';
import blackMarble from './images/black-marble.jpg';


function App() {

  const {socket, socketOpen} = useSocket();
  const {commandSocket, commandSocketOpen} = useCommandSocket();
  const [climateData, setClimateData] = useState(null);
  const [systemData, setSystemData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [networkData, setNetworkData] = useState(null);
  const [image, setImage] = useState(null)

  useEffect(() => {
    if (socketOpen) {
      console.log('listening');
      socket.onmessage = msg => {
        console.log(msg);
        const data = JSON.parse(msg.data);
        // console.log(data);
        if (data === 'ping') {
          socket.send('pong');
        } else if (data.timestamp) {
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

  useEffect(() => {
    if (commandSocketOpen) {
      commandSocket.onmessage = msg => {
        const blob = msg.data;
        console.log(blob);
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function() {
          const result = reader.result
          const base64 = result.replace('data:application/octet-stream;base64,', '');
          console.log(base64);
          setImage(base64);
        }
      };
    }
  }, [commandSocket, commandSocketOpen]);


  return (
    <div className="app">
      <TitleWidget lastUpdated={lastUpdated}></TitleWidget>
      <img src={blackMarble} className="background-img"></img>
      <div className="widget-container">
        <div className="widget-subdivide-1">
          <WeatherWidget climateData={climateData} ></WeatherWidget>
          <PiSystemWidget systemData={systemData} ></PiSystemWidget>
          <NetworkWidget></NetworkWidget>
        </div>
        <div className="widget-subdivide-2">
          <CameraWidget commandSocket={commandSocket} commandSocketOpen={commandSocketOpen} image={image}>
          </CameraWidget>
        </div>
      </div>
    </div>
  );
}

export default App;
