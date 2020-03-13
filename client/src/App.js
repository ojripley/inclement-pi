import React, { useEffect } from 'react';
import './App.css';
import useSocket from './hooks/useSocket';

function App() {

  const {socket, socketOpen} = useSocket();

  useEffect(() => {
    if (socketOpen) {
      socket.onmessage = msg => {
        console.log(JSON.parse(msg.data));
      };
    }
  }, [socket, socketOpen]);

  return (
    <div className="App">
      <header>Inclement-Pi</header>
    </div>
  );
}

export default App;
