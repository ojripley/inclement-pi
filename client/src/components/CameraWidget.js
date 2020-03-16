import React, { useEffect, useState } from 'react';

export default function CameraWidget(props) {

  const requestImage = function() {
    if (props.commandSocketOpen) {
      props.commandSocket.send(JSON.stringify({request: 'image'}));
    }
  }

  return (
    <div className="widget">
      <header>Camera</header>
      <button onClick={requestImage}></button>
    </div>
  )
}