import React, { useEffect, useState } from 'react';
import DataReadout from './DataReadout';

export default function PiSystemWidget(props) {


  const [cpuPercent, setCpuPercent] = useState('');
  const [cpuTemperature, setCpuTemperature] = useState('');
  const [memoryPercent, setMemoryPercent] = useState('');

  useEffect(() => {
    if (props.systemData) {
      setCpuPercent(props.systemData.cpuPercent);
      setCpuTemperature(props.systemData.cpuTemperature);
      setMemoryPercent(props.systemData.memoryPercent);
    }
  }, [props.systemData]);

  return(
    <div className="widget">
      <header className={'widget-header'}>System</header>
      <div className={'data-readout-container'}>
        <DataReadout label={'CPU Temp'} value={cpuTemperature} unit={'C'}></DataReadout>
        <DataReadout label={'CPU Usage'} value={cpuPercent} unit={'%'}></DataReadout>
        <DataReadout label={'Memory Usage'} value={memoryPercent} unit={'Mb/s'}></DataReadout>
        <DataReadout label={'Connected'} value={props.socketOpen === true ? 'yes' : 'no'} unit={''}></DataReadout>
      </div>
    </div>
  )
}