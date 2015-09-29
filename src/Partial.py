#!/usr/bin/env python
# Partial.py - John Burnett & Will Johnson (c)2015
# Class for storing data about partials 
#
# Usage:
# Init with frequency, amplitude, and an (optional) time index
# Call make_inactive() (optional time index) to compute duration
# if no time indicies are given the partial will default to length 1

class Partial():
	
    def __init__(self, frequency, amplitude, time_index=0):
        self.is_active = True
        self.frequency = frequency
        self.duration = 0
        self.amplitude = amplitude
        self.start_time = time_index
        self.end_time = 0
    
    
    def __repr__(self):
        return "<Frequency: %s, Amplitude: %s, Start: %s, End: %s, Duration: %s>" % (self.frequency, self.amplitude, self.start_time, self.end_time, self.duration)
       
        
    def __str__(self):
        return "<Frequency: %s, Amplitude: %s, Start: %s, End: %s, Duration: %s>" % (self.frequency, self.amplitude, self.start_time, self.end_time, self.duration)
    
        
    def make_inactive(self, time_index=1):
        self.end_time = time_index
        self.duration = self.end_time - self.start_time
        self.is_active = False
        
        
    