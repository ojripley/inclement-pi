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
      <header>Weather</header>
      <p>Temperature: {temperature} C</p>
      <p>Humidity: {humidity} %</p>
      <p>Pressure: {pressure} mBar</p>
    </div>
  );
};