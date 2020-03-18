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
      <header className={'widget-header'}>| <span className={'widget-header-text'}>System</span> |</header>
      <p>CPU Temperature: {cpuTemperature} C</p>
      <p>CPU Percent: {cpuPercent} %</p>
      <p>Memory Percent: {memoryPercent} %</p>
      <p>Last Updated: {props.lastUpdated}</p>
    </div>
  )
}