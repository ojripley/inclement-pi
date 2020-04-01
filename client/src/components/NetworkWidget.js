import React, { useState, useEffect } from 'react';

export default function NetworkWidget(props) {

  const [ping, setPing] = useState(null);
  const [download, setDownload] = useState(null);
  const [upload, setUpload] = useState(null);
  

  useEffect(() => {
    if (props.networkData) {
      setPing(props.networkData.ping);
      setDownload(props.networkData.download);
      setUpload(props.networkData.upload);
    }
  }, [props.networkData]);

  const requestNetworkTest = function() {
    if (props.socketOpen) {
      props.socket.send(JSON.stringify({request: 'network-test'}));
    }
  }


  return (
    <div className="widget">
      <header className={'widget-header'}>Network</header>
      <p className={'widget-data-text'} >Ping: {ping} s</p>
      <p className={'widget-data-text'} >Download: {download} Mb/s</p>
      <p className={'widget-data-text'} >Upload: {upload} Mb/s</p>
      <p className={'widget-data-text'} >Receiving Data: {props.socketOpen === true ? 'yes' : 'no'}</p>
      <button onClick={requestNetworkTest}></button>
    </div>
  );
};