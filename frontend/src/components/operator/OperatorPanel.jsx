import React, { useState } from 'react';
import ProductionCounter from './ProductionCounter';
import StatusButtons from './StatusButtons';

const OperatorPanel = ({ machine }) => {
  const [currentStatus, setCurrentStatus] = useState('stopped');
  const [goodParts, setGoodParts] = useState(0);
  const [defectiveParts, setDefectiveParts] = useState(0);

  const handleStatusChange = async (newStatus) => {
    try {
      await machineAPI.sendData(machine.id, {
        status: newStatus,
        current_consumption: null,
        temperature: null,
        pressure: null,
        cycle_count: null
      });
      setCurrentStatus(newStatus);
    } catch (error) {
      console.error('Status update error:', error);
    }
  };

  const handleProductionRecord = async (isGood) => {
    try {
      if (isGood) {
        setGoodParts(prev => prev + 1);
      } else {
        setDefectiveParts(prev => prev + 1);
      }

      // Send production data to API
      await productionAPI.recordProduction({
        machine_id: machine.id,
        good_parts: isGood ? 1 : 0,
        defective_parts: isGood ? 0 : 1
      });
    } catch (error) {
      console.error('Production record error:', error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">{machine.name}</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StatusButtons 
          currentStatus={currentStatus}
          onStatusChange={handleStatusChange}
        />
        
        <ProductionCounter
          goodParts={goodParts}
          defectiveParts={defectiveParts}
          onProductionRecord={handleProductionRecord}
        />
      </div>

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2">Mevcut Durum: {currentStatus}</h3>
        <div className="text-sm text-gray-600">
          İyi Ürün: {goodParts} | Hatalı Ürün: {defectiveParts}
        </div>
      </div>
    </div>
  );
};

export default OperatorPanel;
