import { useState, useEffect, useCallback } from 'react';
import { machineAPI } from '../services/api';
import { webSocketService } from '../services/websocket';

export const useMachineData = (machineId) => {
  const [machine, setMachine] = useState(null);
  const [realTimeData, setRealTimeData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMachine = useCallback(async () => {
    try {
      setLoading(true);
      const response = await machineAPI.getById(machineId);
      setMachine(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [machineId]);

  useEffect(() => {
    fetchMachine();
    
    const handleMachineUpdate = (data) => {
      if (data.machine_id === machineId) {
        setRealTimeData(prev => [...prev.slice(-99), data]);
      }
    };

    webSocketService.on('machine_update', handleMachineUpdate);

    return () => {
      webSocketService.off('machine_update', handleMachineUpdate);
    };
  }, [machineId, fetchMachine]);

  return { machine, realTimeData, loading, error, refetch: fetchMachine };
};
