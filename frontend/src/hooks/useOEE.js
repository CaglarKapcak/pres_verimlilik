import { useState, useEffect, useCallback } from 'react';
import { machineAPI } from '../services/api';

export const useOEE = (machineId, timeRange = 'today') => {
  const [oeeData, setOeeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const calculateTimeRange = useCallback(() => {
    const now = new Date();
    let startTime, endTime;

    switch (timeRange) {
      case 'today':
        startTime = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        endTime = now;
        break;
      case 'shift':
        // 8 saatlik vardiya
        startTime = new Date(now.getTime() - 8 * 60 * 60 * 1000);
        endTime = now;
        break;
      case 'week':
        startTime = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        endTime = now;
        break;
      default:
        startTime = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        endTime = now;
    }

    return {
      start: startTime.toISOString(),
      end: endTime.toISOString()
    };
  }, [timeRange]);

  const fetchOEE = useCallback(async () => {
    if (!machineId) return;

    try {
      setLoading(true);
      const timeRange = calculateTimeRange();
      
      const response = await machineAPI.getOEE(
        machineId, 
        timeRange.start, 
        timeRange.end
      );
      
      setOeeData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('OEE fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [machineId, calculateTimeRange]);

  useEffect(() => {
    fetchOEE();
    
    // Her 5 dakikada bir güncelle
    const interval = setInterval(fetchOEE, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [fetchOEE]);

  const refresh = useCallback(() => {
    fetchOEE();
  }, [fetchOEE]);

  return {
    oeeData,
    loading,
    error,
    refresh,
    timeRange
  };
};
