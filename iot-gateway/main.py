import time
import requests
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
from sensors.current_sensor import CurrentSensor
from sensors.proximity_sensor import ProximitySensor
from sensors.temperature_sensor import TemperatureSensor
from utils.config_reader import ConfigReader

class IoTGateway:
    def __init__(self):
        self.config = ConfigReader().load_config()
        self.setup_sensors()
        self.cycle_count = 0
        self.last_cycle_time = time.time()
        
    def setup_sensors(self):
        # I2C bağlantısı
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        
        # Sensörleri başlat
        self.current_sensor = CurrentSensor(self.ads, ADS.P0)
        self.temperature_sensor = TemperatureSensor(self.ads, ADS.P1)
        self.proximity_sensor = ProximitySensor(pin=17)
        
    def read_sensors(self):
        """Tüm sensörlerden veri oku"""
        return {
            'current': self.current_sensor.read(),
            'temperature': self.temperature_sensor.read(),
            'cycle_detected': self.proximity_sensor.detect_cycle(),
            'cycle_time': self._calculate_cycle_time()
        }
    
    def _calculate_cycle_time(self):
        """Çevrim süresini hesapla"""
        if self.proximity_sensor.detect_cycle():
            current_time = time.time()
            cycle_time = current_time - self.last_cycle_time
            self.last_cycle_time = current_time
            self.cycle_count += 1
            return cycle_time
        return None
    
    def send_data(self, machine_id, sensor_data):
        """Veriyi API'ye gönder"""
        payload = {
            "machine_id": machine_id,
            "current_consumption": sensor_data['current'],
            "temperature": sensor_data['temperature'],
            "cycle_count": self.cycle_count,
            "cycle_time": sensor_data['cycle_time'],
            "status": "running" if sensor_data['current'] > 4.0 else "stopped",
            "timestamp": time.time()
        }
        
        try:
            response = requests.post(
                f"{self.config['api_url']}/api/machines/{machine_id}/data",
                json=payload,
                timeout=2
            )
            
            if response.status_code == 200:
                print(f"✓ Veri gönderildi: {payload}")
            else:
                print(f"✗ Gönderme hatası: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Ağ hatası: {e}")
        except Exception as e:
            print(f"✗ Beklenmeyen hata: {e}")
    
    def run(self):
        """Ana çalıştırma döngüsü"""
        machine_id = self.config['machine_id']
        
        print(f"IoT Gateway başlatıldı. Makine ID: {machine_id}")
        print("Veri gönderimi başlıyor...")
        
        try:
            while True:
                sensor_data = self.read_sensors()
                self.send_data(machine_id, sensor_data)
                time.sleep(self.config['update_interval'])
                
        except KeyboardInterrupt:
            print("\nGateway durduruluyor...")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    gateway = IoTGateway()
    gateway.run()
