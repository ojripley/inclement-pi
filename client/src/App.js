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


function App() {

  const {socket, socketOpen} = useSocket();
  const {commandSocket, commandSocketOpen} = useCommandSocket();
  const [climateData, setClimateData] = useState([]);
  const [systemData, setSystemData] = useState(null);
  const [climateUpdateTimestamp, setClimateUpdateTimestamp] = useState(null);
  const [imageUpdateTimestamp, setImageUpdateTimestamp] = useState(null);
  const [intervalHandle, setIntervalHandle] = useState(0);
  const [lastUpdated, setLastUpdated] = useState(0);
  const [imageLastUpdated, setImageLastUpdated] = useState(0);
  const [networkData, setNetworkData] = useState(null);
  const [currentDate] = useState(new Date());
  const [image, setImage] = useState(null);
  const [quote, setQuote] = useState({
    quote: "Looks like you've exceeded the number of requests to the free quotes API, and I'm not paying for that!",
    author: "Owen Ripley"
  });

  useEffect(() => {
    const tempHandle = setInterval(() => {
      clearInterval(intervalHandle);
      const currentTime = new Date();
      if (climateUpdateTimestamp) {
        setLastUpdated(Math.round((currentTime - climateUpdateTimestamp) / 1000));
      }

      if (imageUpdateTimestamp) {
        setImageLastUpdated(Math.round((currentTime - imageUpdateTimestamp) / 1000));
      }
    }, 1000);

    setIntervalHandle(tempHandle);
  }, [imageUpdateTimestamp]);

  useEffect(() => {
    if (socketOpen) {
      console.log('listening');
      socket.onmessage = msg => {
        const data = JSON.parse(msg.data);
        if (data.climateData) {
          const tempUpdateTimestamp = new Date();
          // console.log(data.climateData);
          // const tempCd = data.climateData;
          // setClimateData(tempCd);
          setClimateData(data.climateData);
          setSystemData(data.systemData);
          setClimateUpdateTimestamp(tempUpdateTimestamp);
        } else {
          console.log('Error: difficulty getting data');
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
          const result = reader.result;
          let base64 = result.replace('data:application/octet-stream;base64,', '');
          while (base64.length % 4 > 0) { // ios does not display base64 images that are not divisible by 4. Use '=' as a filler
            base64 += '=';
          }
          setImage(base64);
          console.log('setting image');
          setImageUpdateTimestamp(new Date());
        }
      };
    }
  }, [commandSocket, commandSocketOpen]);

  useEffect(() => {
    fetch("http://quotes.rest/qod.json", {
      "method": "GET",
    })
      .then(response => {
        response.json().then(body => {
          if (body.contents) {
            setQuote(body.contents.quotes[0]);
          }
        });
      });
  }, []);

  return (
    <>
      <div className='background'></div>
      <div className='app'>
        <div className='widget-container'>
          <div className='widget-subdivide-1'>
            <TitleWidget quote={quote} currentDate={currentDate} ></TitleWidget>
            <PiSystemWidget systemData={systemData} lastUpdated={lastUpdated} ></PiSystemWidget>
            <NetworkWidget></NetworkWidget>
          </div>
          <div className='widget-subdivide-2'>
            <WeatherWidget climateData={climateData} lastUpdated={lastUpdated} ></WeatherWidget>
            <CameraWidget commandSocket={commandSocket} commandSocketOpen={commandSocketOpen} image={image} imageLastUpdated={imageLastUpdated}></CameraWidget>
          </div>
        </div>
      </div>
    </>
  );
};

export default App;
