import React, { useState, useEffect } from 'react';
import { LineChart, AreaChart } from 'react-chartkick';
import 'chart.js';

export default function WeatherWidget(props) {

  const [temperature, setTemperature] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [pressure, setPressure] = useState(null);
  const [graphMode, setGraphMode] = useState('temp');

  useEffect(() => {
    if (props.climateData && props.climateData.length > 0) {
      setTemperature(props.climateData[props.climateData.length - 1].temperature)
      setHumidity(props.climateData[props.climateData.length - 1].humidity);
      setPressure(props.climateData[props.climateData.length - 1].pressure);
    }
  }, [props.climateData]);

  const graphData = {};
  for (let data of props.climateData) {
    if (graphMode === 'temp') {
      graphData[data.timestamp] = data.temperature;
    }
  }

  return (
    <div className='widget'>
      <header className={'widget-header'}>Weather</header>
      <div className='weather-data-container'>
        <div className='weather-readouts'>
          <p className={'widget-data-text'} >Temperature: {temperature} C</p>
          <p className={'widget-data-text'} >Humidity: {humidity} %</p>
          <p className={'widget-data-text'} >Pressure: {pressure} mBar</p>
          <p className={'widget-data-text'} >Last Updated: {props.lastUpdated}</p>
        </div>
        <AreaChart id='weather-chart' colors={["#ffff00", "#000000"]} width="50%" height='50%' data={graphData}></AreaChart>
      </div>
    </div>
  );
};