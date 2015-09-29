#!/usr/bin/env python

class Partial_Tracker():
    
    def __init__ (self, FFT_Analyzer):
        self.fft_analyzer = FFT_Analyzer
        self.length_in_seconds = FFT_Analyzer.length_in_seconds
        self.min_amp = 0.01
        self.modal_model = []
        self.partial_track_data = {}
        self.deviations = [0 , -2.5, 2.5, -5, 5]
    
    
    def partial_track(self):
        #{freq: [[amp, start, end, duration], [amp, start...]]}
        #need to implement some sort of freq deviation param to account for clustering effect
        time_step = self.length_in_seconds / len(self.fft_analyzer.deep_analysis)
        partial_track_dict = {}
        sustaining = []
        for bin in self.fft_analyzer.deep_analysis[0]:
            if bin[1] > self.min_amp:
                sustaining.append([bin[0], 0, 0, bin[1], 0])
                    
        current_time = 0
        for i, window in enumerate(self.fft_analyzer.deep_analysis):
            window_dict = {}
            for bin in window:
                window_dict[bin[0]] = bin[1]
            for partial in sustaining:
                if not(self.still_sustaining(window_dict[partial[0]])):
                    partial[2] = current_time
                    partial[4] = partial[2] - partial[1]
                    if not(partial[0] in partial_track_dict):
                        partial_track_dict[partial[0]] = []
                    partial_track_dict[partial[0]].append(partial[1:])
                    sustaining.remove(partial)
            for bin in window:
                if self.is_onset(bin, sustaining):
                    sustaining.append([bin[0], current_time, 0, bin[1], 0])
            if i == len(self.fft_analyzer.deep_analysis):
                for partial in sustaining:
                    partial[2] = current_time
                    partial[4] = partial[2] - partial[1]
                    partial_track_dict[partial[0]].append(partial[1:])
                    sustaining.remove(partial)
            current_time += time_step
        
        self.partial_track_data = partial_track_dict
        print self.partial_track_data
   
   
    def is_onset(self, bin, sustaining):
        partial_dict = {}
        for partial in sustaining:
            partial_dict[partial[0]] = partial[3]
        if not(bin[0] in partial_dict):
            if bin[1] > self.min_amp: 
                return True
            return False
     
              
    def still_sustaining(self, amp):
        if amp >= self.min_amp:   
            return True
        else: 
            return False
            
                
    def create_freq_dict(self, window):
        freq_dict = {}
        for mode in window:
            freq_dict[mode[0]] = mode[1]
        return freq_dict

    
    def create_modal_model(self):
        modal_model = []
        for freq in self.partial_track_data:
            for instance in self.partial_track_data[freq]:
                if instance[0] == 0:
                    modal_model.append([freq, instance[3], instance[2]])
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