import React, { useState, useEffect } from 'react';
import DataReadout from './DataReadout';

export default function NetworkWidget(props) {

  const [ping, setPing] = useState('');
  const [download, setDownload] = useState('');
  const [upload, setUpload] = useState('');
  const [pendingResults, setPendingResults] = useState(false);
  
  // useEffect(() => {
  //   if (props.commandSocketOpen) {
  //     setTimeout(() => {
  //       props.commandSocket.send(JSON.stringify({ request: 'network-test' }));
  //       setPendingResults(true)
  //     }, 3500);
  //   }
  // }, [props.commandSocketOpen, props.commandSocket]);

  useEffect(() => {
    if (props.networkData) {
      setPendingResults(false);
      setPing(props.networkData.ping);
      setDownload(props.networkData.download);
      setUpload(props.networkData.upload);
    }
  }, [props.networkData]);

  const requestNetworkTest = function() {
    if (props.commandSocketOpen) {
      props.commandSocket.send(JSON.stringify({request: 'network-test'}));
      setPendingResults(true);
    }
  }


  return (
    <div className="widget">
      <header className={'widget-header'}>Network</header>
      <div className={'data-readout-container'}>
        <button onClick={requestNetworkTest} className={pendingResults === true ? 'test-network-button-disabled' : 'test-network-button-enabled'}>Test Network</button>
        <DataReadout label={'Ping'} value={ping} unit={'s'}></DataReadout>
        <DataReadout label={'Download'} value={download} unit={'Mb/s'}></DataReadout>
        <DataReadout label={'Upload'} value={upload} unit={'Mb/s'}></DataReadout>
        <DataReadout label={'Last Updated'} value={props.networkLastUpdated > 60 ? Math.round(props.networkLastUpdated / 60) : props.networkLastUpdated} unit={props.networkLastUpdated > 60 ? 'm' : 's'}></DataReadout>
      </div>
    </div>
  );
};