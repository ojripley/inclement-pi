import React, { useEffect, useState } from 'react';

export default function CameraWidget(props) {

  const requestImage = function() {
    if (props.commandSocketOpen) {
      props.commandSocket.send(JSON.stringify({request: 'image'}));
    }
  }

  useEffect(() => {
    if (props.image) {
      console.log(props.image);
    }
  });

  return (
    <div className="widget">
      <header>View</header>
      <button onClick={requestImage}>Update View</button>
      {props.image ? <img src={'data:image/jpg;base64,' + props.image}></img> : 
      <></>}
    </div>
  )
}