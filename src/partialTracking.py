#!/usr/bin/env python

class Partial_Tracker():
    
    def __init__ (self, fft_data):
        self.max_amp_deviation = 0.2
        self.max_freq_deviation = 10 #hz
        self.minlength = 0.1 #seconds
        self.minamp = 0.001
        self.partial_track = self.track(fft_data)
        self.freq_damp_amp = []
    
    def track(self, fft_data):
        return 1
        