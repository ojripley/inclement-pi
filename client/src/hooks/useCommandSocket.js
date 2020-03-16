import { useState, useEffect } from 'react';

export default function useCommandSocket() {

  // const [socket] = useState(new WebSocket("ws://192.168.1.155:8080/"));
  const [commandSocket, setCommandSocket] = useState(null);
  const [commandSocketOpen, setCommandSocketOpen] = useState(false);

  const serverAddress = "ws://192.168.1.207:9090/";
  // const serverAddress = "ws://192.168.1.155:9090/";

  useEffect(() => {
    setCommandSocket(new WebSocket(serverAddress));
    setCommandSocketOpen(true);
  }, [serverAddress])

  useEffect(() => {
    if (commandSocketOpen) {
      commandSocket.onopen = () => {
        console.log('connection successful');
        commandSocket.send('test');
      }
    }
  }, [commandSocket, commandSocketOpen])

  return {
    commandSocket,
    commandSocketOpen
  };
}