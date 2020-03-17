import React from 'react';

export default function TitleWidget(props) {
  
  return (
    <div className={'title'}>
      <header>Inclement-Pi</header>
      <p>Last Updated: {props.lastUpdated}</p>
    </div>
  );
};