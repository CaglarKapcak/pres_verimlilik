import React, { createContext, useContext, useState, useEffect } from 'react';
import { machineAPI } from '../services/api';

const MachineContext = createContext();

export const useMachines = () => {
  const context = useContext(MachineContext);
  if (!context) {
    throw new Error('useMachines must be used within a MachineProvider');
  }
  return context;
};

export const MachineProvider = ({ children }) => {
  const [machines, setMachines] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMachines();
  }, []);

  const loadMachines = async () => {
    try {
      setLoading(true);
      const response = await machineAPI.getAll();
      setMachines(response.data);
      
      // Varsayılan olarak ilk makineyi seç
      if (response.data.length > 0 && !selectedMachine) {
        setSelectedMachine(response.data[0]);
      }
      
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Machines load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const selectMachine = (machineId) => {
    const machine = machines.find(m => m.id === machineId);
    if (machine) {
      setSelectedMachine(machine);
    }
  };

  const updateMachine = (machineId, updates) => {
    setMachines(prev => prev.map(machine =>
      machine.id === machineId ? { ...machine, ...updates } : machine
    ));
    
    if (selectedMachine && selectedMachine.id === machineId) {
      setSelectedMachine(prev => ({ ...prev, ...updates }));
    }
  };

  const addMachine = (machine) => {
    setMachines(prev => [...prev, machine]);
  };

  const removeMachine = (machineId) => {
    setMachines(prev => prev.filter(machine => machine.id !== machineId));
    
    if (selectedMachine && selectedMachine.id === machineId) {
      setSelectedMachine(null);
    }
  };

  const value = {
    machines,
    selectedMachine,
    loading,
    error,
    selectMachine,
    updateMachine,
    addMachine,
    removeMachine,
    refreshMachines: loadMachines
  };

  return (
    <MachineContext.Provider value={value}>
      {children}
    </MachineContext.Provider>
  );
};
