// Tarih ve saat formatlama
export const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('tr-TR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('tr-TR', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('tr-TR');
};

// Sayı formatlama
export const formatNumber = (number, decimals = 0) => {
  return new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(number);
};

export const formatPercentage = (value, decimals = 1) => {
  return `${formatNumber(value * 100, decimals)}%`;
};

// Süre formatlama
export const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;

  if (hours > 0) {
    return `${hours}sa ${minutes}d`;
  } else if (minutes > 0) {
    return `${minutes}d ${remainingSeconds}s`;
  } else {
    return `${remainingSeconds}s`;
  }
};

// Makine durumu formatlama
export const formatMachineStatus = (status) => {
  const statusMap = {
    'running': { text: 'Çalışıyor', color: 'green' },
    'idle': { text: 'Beklemede', color: 'yellow' },
    'stopped': { text: 'Durduruldu', color: 'red' },
    'maintenance': { text: 'Bakımda', color: 'blue' }
  };

  return statusMap[status] || { text: 'Bilinmiyor', color: 'gray' };
};

// Para formatlama
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('tr-TR', {
    style: 'currency',
    currency: 'TRY'
  }).format(amount);
};
