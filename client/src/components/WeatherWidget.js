import React, { useState, useEffect } from 'react';
import { LineChart, AreaChart } from 'react-chartkick';
import 'chart.js';

export default function WeatherWidget(props) {

  const [temperature, setTemperature] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [pressure, setPressure] = useState(null);
  const [graphMode, setGraphMode] = useState('temp');

  useEffect(() => {
    if (props.climateData) {
      setTemperature(props.climateData.temperature)
      setHumidity(props.climateData.humidity);
      setPressure(props.climateData.pressure);
    }
  }, [props.climateData]);

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
        <div className={'weather-chart'}>
          <AreaChart id='graph' colors={["#ffff00", "#000000"]} height={'100%'} data={props.climateData.hourly_averages}></AreaChart>
          <div className={'button-container'}>
            <button>Temp</button>
            <button>Humidity</button>
            <button>Pressure</button>
          </div>
        </div>
      </div>
    </div>
  );
};