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
        time_step = self.length_in_seconds / len(self.fft_analyzer.deep_analysis)
        
        partial_track_dict = {}
        #{freq: amp, start, end, duration}
        sustaining = []
        for bin in self.fft_analyzer.bins:
            partial_track_dict[bin[0]] = [time_step, bin[1]]
            sustaining.append(bin[0])
        
        #if the mode is still holding add the time_step to the damping factor    
        for window in self.fft_analyzer.deep_analysis:
            for bin in window:
                #print bin
                if (self.in_window(bin[0], modal_model_dict, sustaining)): 
                    partial_track_dict[bin[0]] = [partial_track_dict[bin[0]][0]+time_step,partial_track_dict[bin[0]][1]]
                    
        self.create_modal_model()
        
    
    def create_modal_model(self):
        #save to self - good!
        modal_model = []
        for mode in self.partial_track_data:
            modal_model.append([mode, modal_model_dict[mode][0], modal_model_dict[mode][3]])
        modal_model = amp_sort(modal_model)
        self.modal_model = modal_model
   
   
    def detect_onset(self):
        return
     
              
    def in_window(self, bin_freq, mode_dict, sustaining):
        if bin_freq in mode_dict and bin_freq in sustaining: 
            # && greater than the min amplitude
            if mode_dict[bin_freq] >= self.min_amp:   
                return True
            else:
                sustaining.remove(bin_freq)
        else: 
            return False
            
                
    def create_freq_dict(self, window):
        freq_dict = {}
        for mode in window:
            freq_dict[mode[0]] = mode[1]
        return freq_dict


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