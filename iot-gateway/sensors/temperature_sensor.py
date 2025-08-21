import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class TemperatureSensor:
    def __init__(self, ads, channel):
        self.channel = AnalogIn(ads, channel)
        # PT100 sensörü için kalibrasyon değerleri
        self.calibration = {
            'min_voltage': 0.5,  # 0°C
            'max_voltage': 5.0,  # 500°C
            'min_temp': 0,
            'max_temp': 500
        }
    
    def read(self):
        """Sıcaklık değerini oku ve dönüştür"""
        voltage = self.channel.voltage
        
        # Voltajı sıcaklığa dönüştür (lineer interpolasyon)
        voltage_range = self.calibration['max_voltage'] - self.calibration['min_voltage']
        temp_range = self.calibration['max_temp'] - self.calibration['min_temp']
        
        temperature = self.calibration['min_temp'] + (
            (voltage - self.calibration['min_voltage']) * temp_range / voltage_range
        )
        
        return max(self.calibration['min_temp'], 
                  min(temperature, self.calibration['max_temp']))
    
    def read_raw(self):
        """Ham voltaj değerini oku"""
        return self.channel.voltage
