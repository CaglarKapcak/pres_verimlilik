class CurrentSensor:
    def __init__(self, ads, channel):
        self.channel = AnalogIn(ads, channel)
    
    def read(self):
        # 4-20mA → 1-5V dönüşümü
        voltage = self.channel.voltage
        current = (voltage - 1) * 25  # 1V = 4mA, 5V = 20mA
        return max(0, min(current, 20))  # Sınırları koru
