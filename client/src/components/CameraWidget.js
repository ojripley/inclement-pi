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
      <header>Camera</header>
      <button onClick={requestImage}>Take Picture</button>
      {props.image ? <img source={props.image}></img> : 
      <></>}
    </div>
  )
}