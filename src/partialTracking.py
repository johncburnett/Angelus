#!/usr/bin/env python
# partialTracking.py - John Burnett & Will Johnson (c)2015
# Class for performing tracking partials in FFT analysis and extracting modes
#
# Usage:
# Call partial_track() to get a list of all the files partials
# Partial: <frequency, onset amplitude, start time, end time, duration>
# Call create_modal_model() to get the modal vectors of all partials with start_time == 0

from Partial import *
from progressbar import *

## 11/18/2015 - will - 
## need to fix: after fixing FFT_Analyzer the duration of partials
## became unuiform -- no good. 

class Partial_Tracker():

    def __init__ (self, FFT_Analyzer):
        self.fft_analyzer = FFT_Analyzer
        self.length_in_seconds = FFT_Analyzer.length_in_seconds
        self.min_amp = 0.01
        self.compressed_partial_track = []
        self.partials = []
        self.max_deviation = 30 #hz
    
    
    def is_onset(self, onset_bin, partials):
        """
        Returns true if occuence of a frequency above min_amp and not within max_deviation of active partial
        
        Args:
            bin: list of [frequencies, amplitudes]
            partials: list of partials
        """
        if len(partials) == 0:
            return True 
        else:
            for partial in partials:
                if abs(onset_bin[0] - partial.frequency) < self.max_deviation:
                    if partial.is_active:
                        return False
            return True
        
              
    def is_sustaining(self, partial, window_dict):
        """
        Returns true if partial within max_deviation is found in window_dict
        
        Args:
            partial: <partial>
            window_dict: {freq: amp}
        """
        
        for freq in window_dict:
            if abs(freq-partial.frequency) < self.max_deviation:
                partial.frequency += freq
                partial.frequency /= 2
                return True
        return False
       
            
    def find_centers(self, win_list):
        """
        Picks of the most prominient frequencies from a fft analysis accounting for a mmargin of error max_deviation
        
        Args:
            partial_list: a list of all the bins in this window
        
        """
        # seperate into bands
        #print "finding band center frequencies"
        this_band = []
        bands = []
        for win_bin in win_list:
            if len(this_band) == 0:
                this_band.append(win_bin)
                continue
            if abs(win_bin[0] - this_band[-1][0]) < self.max_deviation:
                this_band.append(win_bin)
            else:
                bands.append(this_band)
                this_band = [] 
        
        new_bands = []
        for band in bands:
            amplitudes = []
            amplitudes_dict = {}
            for win_bin in band:
                amplitudes.append(win_bin[1])
                amplitudes_dict[win_bin[1]] = win_bin[0]
            amplitudes.sort()
            amplitudes.reverse()
            new_bands.append([amplitudes_dict[amplitudes[0]], amplitudes[0]]) 
        
        # remove below audio spectrum
        final_bands = []
        for win_bin in new_bands:
            if win_bin[0] > 20:
                final_bands.append(win_bin)
            
        return final_bands
        
        
    def partial_track(self):
        """
        Tracks the partials of FFT_Analyzer.stft_analysis

        """
        time_step = self.length_in_seconds / len(self.fft_analyzer.stft_analysis)
        current_time = 0
        partials = []
        print "Performing Partial Tracking..."
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.fft_analyzer.stft_analysis)).start()
        
        for i, window in enumerate(self.fft_analyzer.stft_analysis):
            window_freq = {}
            sort_window_freqs = []
            for win_bin in window:
                if win_bin[1] > self.min_amp:
                    sort_window_freqs.append(win_bin[0])
                    window_freq[win_bin[0]] = win_bin[1]
            sort_window_freqs.sort()
            window_partials = []
            for freq in sort_window_freqs:
                window_partials.append([freq, window_freq[freq]])    
            window_partials = self.find_centers(window_partials)
            window_partial_dict = {}
            for partial in window_partials:
                window_partial_dict[partial[0]] = partial[1]

            #onset detection
            for win_bin in window_partials: #not sustaining
                if self.is_onset(win_bin, partials):
                    partials.append(Partial(win_bin[0], win_bin[1], current_time))
                else:
                    for partial in partials:
                        if partial.is_active and partial.start_time != current_time:
                            if not(self.is_sustaining(partial, window_partial_dict)):
                                partial.make_inactive(current_time)            
            
            current_time += time_step
            progress.update(i+1)

        for partial in partials:
            if partial.is_active:
                partial.make_inactive(current_time)
        self.partials = partials
        progress.finish()        
    

    def create_modal_model(self, n_modes):
        """
        Parses partial tracking data into a list of modes
        
        Args:
            n_modes: max number of modes to obtain
        """
        modal_model = []
        for partial in self.partials:
            if partial.start_time == 0:
                modal_model.append([partial.frequency, partial.duration, partial.amplitude])
        modal_model = amp_sort(modal_model)
        if len(modal_model) < n_modes:
            print "less partials than requested modes"
        modal_model = modal_model[:n_modes]
        return modal_model

#---------------------------------------------------------------------
#_Utilities
        
def amp_sort(modal_model):
    """"
    Sorts a modal model by amplitude (loudest modes -> softest modes)
    """
    amplitudes = []
    amp_dict = {}
    for mode in modal_model:
        amplitudes.append(mode[2])
        amp_dict[mode[2]] = [mode[0], mode[1]]
    amplitudes.sort()
    amplitudes.reverse()
    new_modes = []
    for amp in amplitudes:
        new_modes.append([amp_dict[amp][0],amp_dict[amp][1], amp])
    return new_modes