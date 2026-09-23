"""
Option A, Smart Fitness Session Analyzer
"""

import statistics 

from data_generator import generate_fitness_data

# First class for the fitness tracker and its observations
class Observation:
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality
        
    @classmethod
    def from_dict(cls, data):
        # Will get the information from the dictinary which is produced by the generator provided to us
        return cls(
            timestamp=data["timestamp"],
            heart_rate=data["heart_rate"],
            skin_response=data["skin_response"],
            temperature=data["temperature"],
            activity_level=data["activity_level"],
            signal_quality=data["signal_quality"]
        )
        
    @staticmethod
    def is_within_range(value, lower, upper):
        # THis is a static method since it does not depend on the instance itself, 
        # a simple check for value within a range
        if value is None:
            return False
        return lower <= value <= upper
    
    def is_valid(self):
         """Return (True, "") if this observation is usable, else (False, reason)."""
         if self.heart_rate is None or self.skin_response is None:
            return False, "missing value"
         if not self.is_within_range(self.heart_rate, 30, 220):
            return False, "heart rate out of realistic range"
         if not self.is_within_range(self.activity_level, 0, 1):
            return False, "activity level out of range"
         if not self.is_within_range(self.signal_quality, 0, 1):
            return False, "signal quality out of range"
         if self.signal_quality < 0.6:
            return False, "signal quality too low"
         return True, ""
        
        