import React from 'react';

export default function DataReadout(props) {

  return (
    <div className={'data-readout'}>
      <p className={'data-readout-text'}>
        <span className={'data-readout-label'}>{props.label}:</span>
        <span className={props.value === 'yes' ? 'connection-readout-green' : props.value === 'no' ? 'connection-readout-red' : 'data-readout-value'}>{String(props.value)}<span>{props.unit}</span></span>
      </p>
    </div>
  );
};