#!/usr/bin/env python
# partialTracking.py - John Burnett & Will Johnson (c)2015
# Class for performing tracking partials in FFT analysis and extracting modes
#
# Usage:
# TBD
# 
# 

from Partial import *

class Partial_Tracker():
    
    
    ### TO - DO
    # documentation! 
    # extract modal data from partial tracking
    # implement partial class
    
    
    def __init__ (self, FFT_Analyzer):
        self.fft_analyzer = FFT_Analyzer
        self.length_in_seconds = FFT_Analyzer.length_in_seconds
        self.min_amp = 0.05
        self.modal_model = []
        self.compressed_partial_track = []
        self.raw_partial_track_data = {}
        self.partials = []
        self.bandwidth = 5
    
    
    def is_onset(self, bin, partials):
        partial_dict = {}
        for partial in partials:
            partial_dict[partial.frequency] = partial
        if not(bin[0] in partial_dict):
            if bin[1] > self.min_amp: 
                return True
        else: 
            if not(partial_dict[bin[0]].is_active):
                return True
            return False
     
              
    def still_sustaining(self, amp):
        if amp >= self.min_amp:   
            return True
        else: 
            return False
       
            
    def find_centers(self, partial_list):
        # seperate into bands
        this_band = []
        bands = []
        for bin in partial_list:
            if len(this_band) == 0:
                this_band.append(bin)
                continue
            if abs(bin[0] - this_band[-1][0]) < self.bandwidth:
                this_band.append(bin)
            else:
                bands.append(this_band)
                this_band = [] 
        
        new_bands = []
        for band in bands:
            amplitudes = []
            amplitudes_dict = {}
            for bin in band:
                amplitudes.append(bin[1])
                amplitudes_dict[bin[1]] = bin[0]
            amplitudes.sort()
            amplitudes.reverse()
            new_bands.append([amplitudes_dict[amplitudes[0]], amplitudes[0]]) 
        
        # remove below audio spectrum
        final_bands = []
        for bin in new_bands:
            if bin[0] > 20:
                final_bands.append(bin)
            
        return final_bands
    
                
    def partial_track(self):
        #init time counter
        time_step = self.length_in_seconds / len(self.fft_analyzer.deep_analysis)                
        current_time = 0
        partials = []
        #step through the windows
        for i, window in enumerate(self.fft_analyzer.deep_analysis):
            
            #find the partials in this window
            window_freq = {}
            sort_window_freqs = []
            for bin in window:
                if bin[1] > self.min_amp:
                    sort_window_freqs.append(bin[0])
                    window_freq[bin[0]] = bin[1]
            sort_window_freqs.sort()
            window_partials = []
            for freq in sort_window_freqs:
                window_partials.append([freq, window_freq[freq]])    
            window_partials = self.find_centers(window_partials)
            window_freq = {}
            for bin in window_partials:
                window_freq[bin[0]] = bin[1]
            
            #if no longer sustaining then make the partial inactive 
            for partial in partials:
                if not(partial.frequency in window_freq):
                    partial.make_inactive(current_time)
            
            #onset detection
            for bin in window_partials:
                if self.is_onset(bin, partials):
                    partials.append(Partial(bin[0], bin[1], current_time))
                                    
            #account for the end of the file
            if i == len(self.fft_analyzer.deep_analysis):
                for partial in partials:
                    if partial.is_active():
                        partial.make_inactive(current_time)

            current_time += time_step
        #self.raw_partial_track_data = partial_track_dict
        print partials
        
    
    def create_modal_model(self):
        modal_model = []
        for freq in self.raw_partial_track_data:
            for instance in self.raw_partial_track_data[freq]:
                if instance[0] == 0:
                    modal_model.append([freq, instance[3], instance[2]])
        modal_model = amp_sort(modal_model)
        return modal_model

#---------------------------------------------------------------------
#_Utilities
        
def amp_sort(modal_model):
    amplitudes = []
    amp_dict = {}
    for mode in modal_model:
        amplitudes.append(mode[2])
        amp_dict[mode[2]] = [mode[0], mode[1]]
    amplitudes.sort()
    amplitudes.reverse()
    print amplitudes
    new_modes = []
    for amp in amplitudes:
        new_modes.append([amp_dict[amp][0],amp_dict[amp][1], amp])
    return new_modes