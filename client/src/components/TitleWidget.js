import React from 'react';

export default function TitleWidget(props) {
  
  return (
    <div className={'title'}>
      <div className={'title-group'}>
        <header className={'title-text'}>|| <span className={'widget-header-text'}>Inclement-Pi</span> ||</header>
        <p className={'date-text'}>{props.currentDate.toLocaleDateString(undefined, {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>
      <p className={'quote'}>" {props.quote.quote} "</p>
      <p className={'author'}>~ {props.quote.author}</p>
    </div>
  );
};