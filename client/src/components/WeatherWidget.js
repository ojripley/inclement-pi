import React, { useState, useEffect } from 'react';
import { LineChart, AreaChart } from 'react-chartkick';
import 'chart.js';

export default function WeatherWidget(props) {

  const [temperature, setTemperature] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [pressure, setPressure] = useState(null);

  useEffect(() => {
    if (props.climateData) {
      setTemperature(props.climateData[props.climateData.length - 1].temperature)
      setHumidity(props.climateData[props.climateData.length - 1].humidity);
      setPressure(props.climateData[props.climateData.length - 1].pressure);
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
        <AreaChart className='weather-chart' colors={["#111fff", "#000"]}></AreaChart>
      </div>
    </div>
  );
};