import React from 'react';

const StatusButtons = ({ currentStatus, onStatusChange }) => {
  const statusOptions = [
    { value: 'running', label: 'Çalışıyor', color: 'green' },
    { value: 'idle', label: 'Beklemede', color: 'yellow' },
    { value: 'stopped', label: 'Durduruldu', color: 'red' },
    { value: 'maintenance', label: 'Bakım', color: 'blue' },
  ];

  const getButtonClass = (status) => {
    const baseClass = "px-6 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 ";
    
    if (status === currentStatus) {
      return baseClass + `bg-${statusOptions.find(s => s.value === status).color}-600 text-white shadow-lg`;
    }
    
    return baseClass + `bg-${statusOptions.find(s => s.value === status).color}-100 text-${statusOptions.find(s => s.value === status).color}-800 hover:bg-${statusOptions.find(s => s.value === status).color}-200`;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Makine Durumu</h3>
      
      <div className="grid grid-cols-2 gap-3">
        {statusOptions.map((status) => (
          <button
            key={status.value}
            onClick={() => onStatusChange(status.value)}
            className={getButtonClass(status.value)}
          >
            {status.label}
          </button>
        ))}
      </div>

      {/* Mevcut Durum Göstergesi */}
      <div className="mt-4 p-3 rounded-lg bg-gray-100">
        <div className="text-sm text-gray-600">Mevcut Durum:</div>
        <div className={`text-lg font-bold text-${statusOptions.find(s => s.value === currentStatus).color}-600`}>
          {statusOptions.find(s => s.value === currentStatus)?.label || 'Bilinmiyor'}
        </div>
      </div>

      {/* Durum Açıklamaları */}
      <div className="mt-4 text-sm text-gray-600">
        <div className="mb-1">• <span className="font-semibold">Çalışıyor:</span> Makine aktif üretimde</div>
        <div className="mb-1">• <span className="font-semibold">Beklemede:</span> Malzeme veya operatör bekleniyor</div>
        <div className="mb-1">• <span className="font-semibold">Durduruldu:</span> Acil durdurma veya planlı duruş</div>
        <div>• <span className="font-semibold">Bakım:</span> Periyodik bakım veya tamirat</div>
      </div>
    </div>
  );
};

export default StatusButtons;
