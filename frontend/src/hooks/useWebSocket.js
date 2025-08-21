import { useEffect, useRef, useCallback } from 'react';
import { webSocketService } from '../services/websocket';

export const useWebSocket = (machineId, onMessage) => {
  const callbackRef = useRef(onMessage);

  // Callback'i güncelle
  useEffect(() => {
    callbackRef.current = onMessage;
  }, [onMessage]);

  const handleMessage = useCallback((data) => {
    if (callbackRef.current) {
      callbackRef.current(data);
    }
  }, []);

  useEffect(() => {
    // WebSocket bağlantısını başlat
    webSocketService.connect();

    // Mesaj handler'ını ekle
    webSocketService.on('machine_update', handleMessage);
    webSocketService.on('oee_update', handleMessage);

    // Belirli bir makineye subscribe ol
    if (machineId) {
      webSocketService.send('subscribe', { machine_id: machineId });
    }

    return () => {
      // Cleanup
      webSocketService.off('machine_update', handleMessage);
      webSocketService.off('oee_update', handleMessage);
      
      if (machineId) {
        webSocketService.send('unsubscribe', { machine_id: machineId });
      }
    };
  }, [machineId, handleMessage]);

  const sendMessage = useCallback((type, data) => {
    webSocketService.send(type, data);
  }, []);

  return { sendMessage };
};
