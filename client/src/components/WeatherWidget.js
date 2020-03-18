import React, { useState, useEffect } from 'react';

export default function WeatherWidget(props) {

  const [temperature, setTemperature] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [pressure, setPressure] = useState(null);

  useEffect(() => {
    if (props.climateData) {
      setTemperature(props.climateData.temperature)
      setHumidity(props.climateData.humidity);
      setPressure(props.climateData.pressure);
    }
  }, [props.climateData]);

  return (
    <div className="widget">
      <header className={'widget-header'}>Weather</header>
      <p className={'widget-data-text'} >Temperature: {temperature} C</p>
      <p className={'widget-data-text'} >Humidity: {humidity} %</p>
      <p className={'widget-data-text'} >Pressure: {pressure} mBar</p>
      <p className={'widget-data-text'} >Last Updated: {props.lastUpdated}</p>
    </div>
  );
};