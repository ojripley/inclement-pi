import React, { useEffect } from 'react';
import DataReadout from './DataReadout';

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
      <div className={'camera-data-container'}>
        <div className={'camera-control-div'}>
          <DataReadout label={'Last Updated'} value={ props.imageLastUpdated > 60 ? Math.round(props.imageLastUpdated / 60) : props.imageLastUpdated } unit={props.imageLastUpdated > 60 ? 'm' : 's'}></DataReadout>
          <button className={'camera-button'} onClick={requestImage}>Update View</button>
        </div>
        {props.image ? <img className={'camera-image'} src={'data:image/jpg;charset=utf-8;base64,' + props.image} alt={'camera view image'} ></img> : 
          <></>}
      </div>
    </div>
  );
};