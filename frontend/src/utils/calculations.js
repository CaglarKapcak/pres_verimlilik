// OEE hesaplama yardımcı fonksiyonları
export const calculateOEE = (availability, performance, quality) => {
  return availability * performance * quality;
};

export const formatOEE = (value) => {
  return Math.round(value * 100);
};

export const getOEEStatus = (oee) => {
  if (oee >= 0.85) return { color: 'green', label: 'Mükemmel' };
  if (oee >= 0.60) return { color: 'yellow', label: 'İyi' };
  if (oee >= 0.40) return { color: 'orange', label: 'Orta' };
  return { color: 'red', label: 'Zayıf' };
};

// Verimlilik metrikleri
export const calculateAvailability = (plannedProductionTime, downtime) => {
  return (plannedProductionTime - downtime) / plannedProductionTime;
};

export const calculatePerformance = (idealCycleTime, totalProduction, operatingTime) => {
  const idealProduction = operatingTime / idealCycleTime;
  return totalProduction / idealProduction;
};

export const calculateQuality = (goodParts, totalParts) => {
  return goodParts / totalParts;
};

// Zaman dönüşümleri
export const secondsToHours = (seconds) => {
  return seconds / 3600;
};

export const hoursToSeconds = (hours) => {
  return hours * 3600;
};

// Veri analizi
export const calculateTrend = (data) => {
  if (!data || data.length < 2) return 0;
  
  const first = data[0];
  const last = data[data.length - 1];
  
  return ((last - first) / first) * 100;
};

export const calculateAverage = (data) => {
  if (!data || data.length === 0) return 0;
  return data.reduce((sum, value) => sum + value, 0) / data.length;
};
