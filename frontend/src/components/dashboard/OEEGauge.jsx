import React from 'react';

const OEEGauge = ({ value, size = 120, strokeWidth = 10 }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const progress = value * circumference;
  
  const getColor = (val) => {
    if (val >= 0.85) return '#10B981'; // green
    if (val >= 0.60) return '#F59E0B'; // yellow
    return '#EF4444'; // red
  };

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E5E7EB"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={getColor(value)}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeLinecap="round"
          className="transition-all duration-300"
        />
      </svg>
      <div className="text-center mt-4">
        <div className="text-2xl font-bold text-gray-900">
          {Math.round(value * 100)}%
        </div>
        <div className="text-sm text-gray-600">OEE</div>
      </div>
    </div>
  );
};

export default OEEGauge;
