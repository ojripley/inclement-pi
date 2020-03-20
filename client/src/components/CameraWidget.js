import React, { useEffect, useState } from 'react';

export default function CameraWidget(props) {

  const requestImage = function() {
    if (props.commandSocketOpen) {
      props.commandSocket.send(JSON.stringify({request: 'image'}));
    }
  };

  useEffect(() => {
    if (props.commandSocketOpen) {
      props.commandSocket.send(JSON.stringify({ request: 'image' }));
    }
  }, [props.commandSocketOpen, props.commandSocket]);

  return (
    <div className="widget">
      <header className={'widget-header'}>Camera View</header>
      <div className={'camera-control-div'}>
        <p className={'widget-data-text'} >Last Updated: {props.imageLastUpdated}</p>
        <button className={'camera-button'} onClick={requestImage}>Update View</button>
      </div>
      {props.image ? <img className={'camera-image'} src={'data:image/jpg;base64,' + props.image}></img> : 
      <></>}
    </div>
  );
};