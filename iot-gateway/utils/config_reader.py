import json
import os
from typing import Dict, Any

class ConfigReader:
    def __init__(self, config_file='gateway_config.json'):
        self.config_file = config_file
        self.default_config = {
            'machine_id': 1,
            'api_url': 'http://localhost:8000',
            'update_interval': 1,  # seconds
            'sensors': {
                'current': {'enabled': True, 'pin': 0},
                'temperature': {'enabled': True, 'pin': 1},
                'proximity': {'enabled': True, 'pin': 17}
            },
            'log_level': 'INFO',
            'max_retries': 3,
            'retry_delay': 5  # seconds
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Konfigürasyon dosyasını yükle"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**self.default_config, **config}
            except (json.JSONDecodeError, IOError) as e:
                print(f"Config file error: {e}. Using default configuration.")
                return self.default_config
        else:
            print("Config file not found. Using default configuration.")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]):
        """Konfigürasyon dosyasını kaydet"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print("Configuration saved successfully.")
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get_sensor_config(self, sensor_name: str) -> Dict[str, Any]:
        """Belirli bir sensörün konfigürasyonunu getir"""
        config = self.load_config()
        return config['sensors'].get(sensor_name, {})
    
    def update_config(self, updates: Dict[str, Any]):
        """Konfigürasyonu güncelle"""
        config = self.load_config()
        config.update(updates)
        self.save_config(config)
