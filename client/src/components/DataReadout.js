import React from 'react';

export default function DataReadout(props) {

  return (
    <div className={'data-readout'}>
      <p className={'data-readout-label'}>{props.label}: <span className={'data-readout-value'}>{props.value}</span></p>
    </div>
  );
};