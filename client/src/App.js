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

  const { socket, socketOpen, setSocket, setSocketOpen} = useSocket();
  const {commandSocket, commandSocketOpen, setCommandSocket, setCommandSocketOpen} = useCommandSocket();
  const [climateData, setClimateData] = useState([]);
  const [systemData, setSystemData] = useState(null);
  const [climateUpdateTimestamp, setClimateUpdateTimestamp] = useState(null);
  const [imageUpdateTimestamp, setImageUpdateTimestamp] = useState(null);
  const [networkUpdateTimestamp, setNetworkUpdateTimestamp] = useState(null);
  const [intervalHandle, setIntervalHandle] = useState(0);
  const [lastUpdated, setLastUpdated] = useState(0);
  const [imageLastUpdated, setImageLastUpdated] = useState(0);
  const [networkLastUpdated, setNetworkLastUpdated] = useState(0);
  const [networkData, setNetworkData] = useState(null);
  const [currentDate] = useState(new Date());
  const [image, setImage] = useState(null);
  const [quote, setQuote] = useState({
    quote: "Looks like you've exceeded the number of requests to the free quotes API, and I'm not paying for that!",
    author: "Owen Ripley"
  });

  const reconnect = function(socketType) {
    if (socketType === 'socket') {
      console.log('attempt reconnect of socket');
      setSocket(setSocket(new WebSocket("ws://192.168.1.155:8080/")));
    }
  }

  useEffect(() => {
    setInterval(() => {
      if (!socketOpen) {
        reconnect('socket');
      }
      // if (!commandSocketOpen) {
      //   console.log('attempt reconnect of command socket');
      //   setCommandSocket(new WebSocket("ws://192.168.1.155:9090/"));
      // }
    }, 1000);
  }, []);

  useEffect(() => {
    const tempHandle = setInterval(() => {
      clearInterval(intervalHandle);
      const currentTime = new Date();
      if (imageUpdateTimestamp) {
        setImageLastUpdated(Math.round((currentTime - imageUpdateTimestamp) / 1000));
      }

      if (networkUpdateTimestamp) {
        setNetworkLastUpdated(Math.round((currentTime - networkUpdateTimestamp) / 1000));
      }
    }, 1000);

    setIntervalHandle(tempHandle);
  }, [imageUpdateTimestamp, networkUpdateTimestamp]);

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
    if (socketOpen) {
      socket.onclose = event => {
        console.log(event);
        setSocketOpen(false);
      }
    }

    if (commandSocketOpen) {
      commandSocket.onclose = event => {
        console.log(event);
        setCommandSocketOpen(false);
      }
    }
  }, [socket, socketOpen, commandSocket, commandSocketOpen]);

  useEffect(() => {
    if (commandSocketOpen) {
      commandSocket.onmessage = msg => {
        console.log(msg);
        if (msg.data instanceof Blob) { // is an image
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
        } else {
          const data = JSON.parse(msg.data);

          if (data.type === 'network-results') {
            setNetworkData(data.data);
            setNetworkUpdateTimestamp(new Date());
          }
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
            <PiSystemWidget systemData={systemData} lastUpdated={lastUpdated} socketOpen={socketOpen} commandSocketOpen={commandSocketOpen} ></PiSystemWidget>
            <NetworkWidget commandSocketOpen={commandSocketOpen} commandSocket={commandSocket} networkData={networkData} networkLastUpdated={networkLastUpdated}></NetworkWidget>
          </div>
          <div className='widget-subdivide-2'>
            <WeatherWidget climateData={climateData} lastUpdated={lastUpdated} socketOpen={socketOpen} ></WeatherWidget>
            <CameraWidget commandSocket={commandSocket} commandSocketOpen={commandSocketOpen} image={image} imageLastUpdated={imageLastUpdated}></CameraWidget>
          </div>
        </div>
      </div>
    </>
  );
};

export default App;
