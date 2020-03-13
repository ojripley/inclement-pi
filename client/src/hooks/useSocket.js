import { useState, useEffect } from 'react';

// const PORT = 8080;
// const HOST = localhost;

export default function useSocket() {

  const [socket] = useState(new WebSocket("ws://localhost:8080/"));
  const [socketOpen, setSocketOpen] = useState(null);

  useEffect(() => {
    console.log('socket');
    console.log(socket);
    socket.onopen = () => {
      setSocketOpen(true);
    }
  })
  
  return {
    socket,
    socketOpen
  };
}