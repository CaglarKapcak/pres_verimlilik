import RPi.GPIO as GPIO
import time

class ProximitySensor:
    def __init__(self, pin=17):
        self.pin = pin
        self.setup()
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self.last_state = GPIO.input(self.pin)
        self.cycle_count = 0
    
    def detect_cycle(self):
        """Çevrim tespiti yap"""
        current_state = GPIO.input(self.pin)
        
        # Yükselen kenar tespiti (0 -> 1)
        if self.last_state == 0 and current_state == 1:
            self.cycle_count += 1
            self.last_state = current_state
            return True
        
        self.last_state = current_state
        return False
    
    def get_cycle_count(self):
        return self.cycle_count
    
    def reset_cycle_count(self):
        self.cycle_count = 0
    
    def cleanup(self):
        GPIO.cleanup()
