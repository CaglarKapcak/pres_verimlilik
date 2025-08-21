import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.database import MachineData

class DataService:
    @staticmethod
    def get_machine_data_history(db: Session, machine_id: int, hours: int = 24) -> List[Dict]:
        """Makine veri geçmişini getir"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        data = db.query(MachineData).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time)
        ).order_by(MachineData.timestamp.asc()).all()
        
        return [
            {
                "timestamp": record.timestamp,
                "status": record.status,
                "current_consumption": record.current_consumption,
                "temperature": record.temperature,
                "cycle_count": record.cycle_count
            }
            for record in data
        ]
    
    @staticmethod
    def analyze_energy_consumption(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> Dict:
        """Enerji tüketim analizi"""
        data = db.query(MachineData).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time),
            MachineData.current_consumption.isnot(None)
        ).all()
        
        if not data:
            return None
        
        # Voltaj değeri (380V tipik endüstriyel voltaj)
        voltage = 380
        
        current_values = [record.current_consumption for record in data]
        power_values = [current * voltage for current in current_values]
        
        total_energy = sum(power_values) / 1000  # kWh
        avg_power = sum(power_values) / len(power_values) if power_values else 0
        max_power = max(power_values) if power_values else 0
        
        return {
            "total_energy_kwh": round(total_energy, 2),
            "average_power_kw": round(avg_power / 1000, 2),
            "max_power_kw": round(max_power / 1000, 2),
            "data_points": len(data)
        }
    
    @staticmethod
    def detect_anomalies(db: Session, machine_id: int, window_hours: int = 1) -> List[Dict]:
        """Anomali tespiti"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=window_hours)
        
        data = db.query(MachineData).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time),
            MachineData.current_consumption.isnot(None)
        ).order_by(MachineData.timestamp.asc()).all()
        
        if len(data) < 10:  # Yeterli veri yoksa
            return []
        
        currents = [record.current_consumption for record in data]
        
        # Basit anomali tespiti (z-score based)
        import numpy as np
        mean_current = np.mean(currents)
        std_current = np.std(currents)
        
        anomalies = []
        for i, record in enumerate(data):
            if std_current > 0:  # Avoid division by zero
                z_score = abs((record.current_consumption - mean_current) / std_current)
                if z_score > 2.5:  # 2.5 standart sapma dışı
                    anomalies.append({
                        "timestamp": record.timestamp,
                        "current": record.current_consumption,
                        "z_score": round(z_score, 2),
                        "severity": "high" if z_score > 3 else "medium"
                    })
        
        return anomalies
