import React, { useEffect, useState } from 'react';

export default function PiSystemWidget(props) {


  const [cpuPercent, setCpuPercent] = useState(null);
  const [cpuTemperature, setCpuTemperature] = useState(null);
  const [memoryPercent, setMemoryPercent] = useState(null);

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
      <p className={'widget-data-text'} >CPU Temperature: {cpuTemperature} C</p>
      <p className={'widget-data-text'} >CPU Usage: {cpuPercent} %</p>
      <p className={'widget-data-text'} >Memory Usage: {memoryPercent} %</p>
      <p className={'widget-data-text'} >Receiving Data: {props.socketOpen === true ? 'yes' : 'no'}</p>
    </div>
  )
}