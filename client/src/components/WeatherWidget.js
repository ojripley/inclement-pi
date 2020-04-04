import React, { useState, useEffect } from 'react';
import { LineChart, AreaChart } from 'react-chartkick';
import 'chart.js';
import DataReadout from './DataReadout';

export default function WeatherWidget(props) {

  const [temperature, setTemperature] = useState('');
  const [humidity, setHumidity] = useState('');
  const [pressure, setPressure] = useState(null);
  const [graphMode, setGraphMode] = useState('temperature');
  const [graphData, setGraphData] = useState({});

  useEffect(() => {
    if (props.climateData.temperature) {
      setTemperature(props.climateData.temperature)
      setHumidity(props.climateData.humidity);
      setPressure(props.climateData.pressure);
    }
  }, [props.climateData]);

  useEffect(() => {
    if (props.climateData.hourly_averages) {
      const now = new Date();
      const currentHour = now.getHours();
      const tempGraphDataToday = {
        name: 'Today',
        data: {}
      };
      const tempGraphDataYesterday = {
        name: 'Yesterday',
        data: {}
      };
      for (let i in props.climateData.hourly_averages) {
        if (i <= currentHour) {
          tempGraphDataToday.data[i] = props.climateData.hourly_averages[i][graphMode];
        } else {
          tempGraphDataYesterday.data[i] = props.climateData.hourly_averages[i][graphMode];
        }
      }

      setGraphData([tempGraphDataToday, tempGraphDataYesterday]);
    }
  }, [graphMode, props.climateData.hourly_averages]);

  return (
    <div className='widget'>
      <header className={'widget-header'}>Weather</header>
      <div className='weather-data-container'>
        <div className='weather-readouts'>
          <DataReadout label={'Temperature'} value={temperature} unit={'C'}></DataReadout>
          <DataReadout label={'Humidity'} value={humidity} unit={'%'}></DataReadout>
          <DataReadout label={'Connected'} value={props.socketOpen === true ? 'yes' : 'no' } unit={''}></DataReadout>
        </div>
        <div className={'weather-chart'}>
          <div className={'chart-container'}>
            <p className={'yaxis-title'}>{graphMode === 'temperature' ? 'C' : graphMode === 'humidity' ? '%' : graphMode === 'pressure' ? 'MB' : ''}</p>
            <AreaChart colors={["#ffff00", '#9F41BE']} height={'100%'} data={graphData} ></AreaChart>
          </div>
          <div className={'weather-button-container'}>
            <button className={graphMode === 'temperature' ? 'graph-button-selected' : 'graph-button-unselected'} onClick={() => setGraphMode('temperature')} >Temperature</button>
            <button className={graphMode === 'humidity' ? 'graph-button-selected' : 'graph-button-unselected'} onClick={() => setGraphMode('humidity')} >Humidity</button>
          </div>
        </div>
      </div>
    </div>
  );
};