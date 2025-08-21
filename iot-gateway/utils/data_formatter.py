import json
from datetime import datetime
from typing import Dict, Any

class DataFormatter:
    @staticmethod
    def format_machine_data(machine_id: int, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sensör verilerini API formatına dönüştür"""
        return {
            'machine_id': machine_id,
            'status': DataFormatter._determine_status(sensor_data),
            'current_consumption': sensor_data.get('current'),
            'temperature': sensor_data.get('temperature'),
            'cycle_count': sensor_data.get('cycle_count', 0),
            'cycle_time': sensor_data.get('cycle_time'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _determine_status(sensor_data: Dict[str, Any]) -> str:
        """Sensör verilerine göre makine durumunu belirle"""
        current = sensor_data.get('current', 0)
        
        if current > 4.0:  # 4mA altındaysa makine durmuş demektir
            return 'running'
        elif current > 0:  # Akım var ama üretim yok
            return 'idle'
        else:
            return 'stopped'
    
    @staticmethod
    def create_downtime_payload(machine_id: int, reason: str, category: str) -> Dict[str, Any]:
        """Duruş verisi payload'ı oluştur"""
        return {
            'machine_id': machine_id,
            'reason': reason,
            'category': category,
            'start_time': datetime.utcnow().isoformat(),
            'operator_id': None  # IoT gateway operator bilgisi olmayabilir
        }
    
    @staticmethod
    def format_for_logging(data: Dict[str, Any]) -> str:
        """Loglama için veriyi formatla"""
        return json.dumps({
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }, indent=2)
