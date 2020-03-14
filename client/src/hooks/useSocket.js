import { useState, useEffect } from 'react';

// const PORT = 8080;
// const HOST = localhost;

export default function useSocket() {

  const [socket] = useState(new WebSocket("ws://192.168.1.155:8080/"));
  const [socketOpen, setSocketOpen] = useState(null);

  useEffect(() => {
    console.log('socket');
    console.log(socket);
    socket.onopen = () => {
      setSocketOpen(true);
      console.log('connection successful');
    }
  })
  
  return {
    socket,
    socketOpen
  };
}