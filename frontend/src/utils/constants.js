// Makine tipleri
export const MACHINE_TYPES = {
  PRESS: 'press',
  WELDING: 'welding',
  INJECTION: 'injection'
};

// Makine tipleri Türkçe karşılıkları
export const MACHINE_TYPE_LABELS = {
  [MACHINE_TYPES.PRESS]: 'Pres Makinesi',
  [MACHINE_TYPES.WELDING]: 'Kaynak Makinesi',
  [MACHINE_TYPES.INJECTION]: 'Enjeksiyon Makinesi'
};

// Durum renkleri
export const STATUS_COLORS = {
  running: '#10B981', // green
  idle: '#F59E0B',    // yellow
  stopped: '#EF4444', // red
  maintenance: '#3B82F6' // blue
};

// OEE hedef değerleri
export const OEE_TARGETS = {
  WORLD_CLASS: 0.85,
  GOOD: 0.60,
  AVERAGE: 0.40,
  POOR: 0.00
};

// Vardiya bilgileri
export const SHIFTS = [
  { id: 1, name: 'A Vardiyası', start: '06:00', end: '14:00' },
  { id: 2, name: 'B Vardiyası', start: '14:00', end: '22:00' },
  { id: 3, name: 'C Vardiyası', start: '22:00', end: '06:00' }
];

// Duruş nedenleri kategorileri
export const DOWNTIME_CATEGORIES = {
  MECHANICAL: 'mechanical',
  ELECTRICAL: 'electrical',
  OPERATIONAL: 'operational',
  QUALITY: 'quality',
  OTHER: 'other'
};

export const DOWNTIME_CATEGORY_LABELS = {
  [DOWNTIME_CATEGORIES.MECHANICAL]: 'Mekanik',
  [DOWNTIME_CATEGORIES.ELECTRICAL]: 'Elektrik',
  [DOWNTIME_CATEGORIES.OPERATIONAL]: 'Operasyonel',
  [DOWNTIME_CATEGORIES.QUALITY]: 'Kalite',
  [DOWNTIME_CATEGORIES.OTHER]: 'Diğer'
};

// API endpointleri
export const API_ENDPOINTS = {
  MACHINES: '/api/machines',
  MACHINE_DATA: '/api/machines/{id}/data',
  PRODUCTION: '/api/production',
  OEE: '/api/machines/{id}/oee',
  AUTH: '/api/auth/token'
};

// LocalStorage keyleri
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER: 'user',
  MACHINE_PREFERENCES: 'machine_preferences'
};

// Chart renkleri
export const CHART_COLORS = [
  '#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6',
  '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
];
