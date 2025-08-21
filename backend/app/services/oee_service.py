from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.database import MachineData, ProductionData, DowntimeReason

class OEEService:
    @staticmethod
    def calculate_availability(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> float:
        # Planlanan üretim süresi
        planned_time = (end_time - start_time).total_seconds()
        
        # Çalışma süresi
        running_data = db.query(MachineData).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time),
            MachineData.status == "running"
        ).all()
        
        running_seconds = sum(
            (min(record.timestamp, end_time) - max(record.timestamp, start_time)).total_seconds()
            for record in running_data
        )
        
        # Duruş süresi
        downtime_records = db.query(DowntimeReason).filter(
            DowntimeReason.machine_id == machine_id,
            DowntimeReason.start_time.between(start_time, end_time)
        ).all()
        
        downtime_seconds = sum(
            (record.end_time - record.start_time).total_seconds() if record.end_time
            else (end_time - record.start_time).total_seconds()
            for record in downtime_records
        )
        
        availability = (planned_time - downtime_seconds) / planned_time
        return max(0, min(availability, 1.0))

    @staticmethod
    def calculate_performance(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> float:
        # Ideal çevrim süresi
        machine = db.query(Machine).filter(Machine.id == machine_id).first()
        ideal_cycle_time = machine.ideal_cycle_time if machine else 1.0
        
        # Toplam çevrim sayısı
        total_cycles = db.query(MachineData.cycle_count).filter(
            MachineData.machine_id == machine_id,
            MachineData.timestamp.between(start_time, end_time)
        ).scalar() or 0
        
        # Planlanan çevrim sayısı
        running_time = (end_time - start_time).total_seconds()
        planned_cycles = running_time / ideal_cycle_time
        
        performance = total_cycles / planned_cycles if planned_cycles > 0 else 0
        return max(0, min(performance, 1.0))

    @staticmethod
    def calculate_quality(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> float:
        # Üretim verileri
        production_data = db.query(ProductionData).filter(
            ProductionData.machine_id == machine_id,
            ProductionData.shift_date >= start_time.date(),
            ProductionData.shift_date <= end_time.date()
        ).all()
        
        total_good = sum(data.good_parts for data in production_data)
        total_defective = sum(data.defective_parts for data in production_data)
        total_parts = total_good + total_defective
        
        quality = total_good / total_parts if total_parts > 0 else 1.0
        return max(0, min(quality, 1.0))

    @staticmethod
    def calculate_oee(db: Session, machine_id: int, start_time: datetime, end_time: datetime) -> dict:
        availability = OEEService.calculate_availability(db, machine_id, start_time, end_time)
        performance = OEEService.calculate_performance(db, machine_id, start_time, end_time)
        quality = OEEService.calculate_quality(db, machine_id, start_time, end_time)
        
        oee = availability * performance * quality
        
        return {
            "availability": availability,
            "performance": performance,
            "quality": quality,
            "oee": oee,
            "timestamp": datetime.utcnow()
        }
