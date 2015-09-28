#!/usr/bin/env python

class Partial_Tracker():
    
    def __init__ (self, FFT_Analyzer):
        self.fft_analyzer = FFT_Analyzer
        self.length_in_seconds = FFT_Analyzer.length_in_seconds
        self.max_amp_deviation = 0.2
        self.max_freq_deviation = 10 #hz
        self.min_amp = 0.01
        self.modal_model = []
        self.partial_track_data = {}
    
    
    def partial_track(self):
        #{freq: [[amp, start, end, duration], [amp, start...]]}
        time_step = self.length_in_seconds / len(self.fft_analyzer.deep_analysis)
        partial_track_dict = {}
        sustaining = []
        current_time = 0
        for window in self.fft_analyzer.deep_analysis:
            for bin in window:
                partial_track_dict[bin[0]] = []
                sustaining.append([bin[0], 0, 0, 0, 0])
        
        for window in self.fft_analyzer.deep_analysis:
            for partial in sustaining:
                if self.still_sustaining(partial):
                    
            current_time += time_step
                       
        self.create_modal_model()
   
   
    def is_onset(self, bin):
        if bin[1] > min_amp: 
            return True
     
              
    def still_sustaining(self, partial):
        if partial[1] >= self.min_amp:   
                return True
        else: 
            return False
            
                
    def create_freq_dict(self, window):
        freq_dict = {}
        for mode in window:
            freq_dict[mode[0]] = mode[1]
        return freq_dict

    
    def create_modal_model(self):
        #save to self - good!
        modal_model = []
        for mode in self.partial_track_data:
            modal_model.append([mode, modal_model_dict[mode][0], modal_model_dict[mode][3]])
        modal_model = amp_sort(modal_model)
        self.modal_model = modal_model

#---------------------------------------------------------------------
#_Utilities
        
def amp_sort(modal_model):
    amplitudes = []
    amp_dict = {}
    for mode in modal_model:
        amplitudes.append(mode[2])
        amp_dict[mode[2]] = [mode[0], mode[1]]
    amplitudes.sort()
    new_modes = []
    for amp in amplitudes:
        new_modes.append([amp_dict[amp][0],amp_dict[amp][1], amp])
    new_modes.reverse()
    return new_modes