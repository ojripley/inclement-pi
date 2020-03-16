import { useState, useEffect } from 'react';

export default function useSocket() {

  // const [socket] = useState(new WebSocket("ws://192.168.1.155:8080/"));
  const [socket, setSocket] = useState(null);
  const [socketOpen, setSocketOpen] = useState(false);

  // const serverAddress = "ws://192.168.1.207:8080/";
  const serverAddress = "ws://192.168.1.155:8080/";

  useEffect(() => {
    setSocket(new WebSocket(serverAddress));
    setSocketOpen(true);
  }, [serverAddress])

  useEffect(() => {
    if (socketOpen) {
      socket.onopen = () => {
        console.log('connection successful');
      }
    }
  }, [socket, socketOpen])
  
  return {
    socket,
    socketOpen
  };
}