from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List
from .database import MachineData, ProductionData, DowntimeReason

class CalculationService:
    @staticmethod
    def calculate_shift_efficiency(db: Session, machine_id: int, shift_date: str, shift_number: int) -> Dict:
        """Vardiya bazlı verimlilik hesapları"""
        production_data = db.query(ProductionData).filter(
            ProductionData.machine_id == machine_id,
            ProductionData.shift_date == shift_date,
            ProductionData.shift_number == shift_number
        ).first()
        
        if not production_data:
            return None
        
        total_parts = production_data.good_parts + production_data.defective_parts
        quality_rate = production_data.good_parts / total_parts if total_parts > 0 else 0
        
        # Vardiya süresi (8 saat)
        shift_duration = 8 * 3600  # seconds
        ideal_cycle_time = 2.5  # seconds, makineden alınabilir
        
        planned_production = shift_duration / ideal_cycle_time
        performance_rate = total_parts / planned_production if planned_production > 0 else 0
        
        return {
            "quality_rate": quality_rate,
            "performance_rate": performance_rate,
            "total_parts": total_parts,
            "good_parts": production_data.good_parts,
            "defective_parts": production_data.defective_parts
        }
    
    @staticmethod
    def calculate_machine_utilization(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> float:
        """Makine kullanım oranını hesapla"""
        total_time = (end_time - start_time).total_seconds()
        
        running_time = db.query(MachineData).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time),
            MachineData.status == "running"
        ).count()
        
        return running_time / total_time if total_time > 0 else 0
    
    @staticmethod
    def predict_maintenance(db: Session, machine_id: int) -> Dict:
        """Tahmini bakım zamanını hesapla"""
        # Son bakım tarihini al
        machine = db.query(Machine).filter(Machine.id == machine_id).first()
        if not machine or not machine.last_maintenance:
            return None
        
        # Ortalama arıza sıklığını hesapla
        downtime_count = db.query(DowntimeReason).filter(
            DowntimeReason.machine_id == machine_id,
            DowntimeReason.category == "mechanical"
        ).count()
        
        # Basit tahmin modeli
        days_since_maintenance = (datetime.now().date() - machine.last_maintenance.date()).days
        
        if downtime_count > 0:
            avg_downtime_interval = days_since_maintenance / downtime_count
            predicted_maintenance = machine.last_maintenance + timedelta(days=avg_downtime_interval * 0.8)
        else:
            predicted_maintenance = machine.last_maintenance + timedelta(days=30)  Default 30 gün
        
        return {
            "last_maintenance": machine.last_maintenance,
            "predicted_maintenance": predicted_maintenance,
            "urgency": "high" if datetime.now().date() > predicted_maintenance.date() else "medium"
        }
