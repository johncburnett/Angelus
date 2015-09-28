#!/usr/bin/env python

from scipy.fftpack import fft, ifft
from numpy import absolute
from numpy import array_split
from copy import deepcopy
from WAV_Reader import WAV_Reader
from partialTracking import Partial_Tracker

class FFT_Analyzer:

    def __init__(self, wav_file, n_points=8192):
        self.wav_name = wav_file
        self.wav_data = []
        self.wav_sample_rate = 44100
        self.length_in_seconds = 0
        self.fft_data = []
        self.fft_n_points = n_points
        self.bins = []
        self.deep_analysis = []
        self.modal_model = []

    
    def get_length_in_seconds(self):
        self.length_in_seconds = float(len(self.wav_data)/self.wav_sample_rate)
    
    
    def extract_samples(self):
        wav_extract = WAV_Reader(self.wav_name)
        wav_extract.toMono()
        self.wav_data = wav_extract.data
        self.wav_sample_rate = wav_extract.sampleRate


    def fft_analysis(self):
        self.fft_data = list(fft(self.wav_data, self.fft_n_points))


    def generate_bins(self):
        magnitudes = fft_to_magnitude(self.fft_data)
        freq_res = self.wav_sample_rate / self.fft_n_points
        num_bins = self.fft_n_points / 2

        for i in range(1,num_bins):
            self.bins.append([freq_res*i, magnitudes[i]])


    def normalize_amplitudes(self):
        self.bins = normalize(self.bins)

         
    def n_loudest_partials(self, n=100):
        self.bins = loudest_partials(self.bins, n)
        

    def perform_analysis(self):
        self.extract_samples()
        self.get_length_in_seconds()
        self.fft_analysis()
        self.generate_bins()
        self.normalize_amplitudes()
        #self.n_loudest_partials()


    def perform_deep_analysis(self, n_samples, n_partials):
        split_wav_samples = array_split(self.wav_data, n_samples)
        split_wav_samples = [list(l) for l in split_wav_samples]
        fft_samples = []
        for l in split_wav_samples:
            fft_of_sample = self.fft_data = list(fft(l, self.fft_n_points))
            fft_samples.append(fft_of_sample)
        magnitudes = [fft_to_magnitude(l) for l in fft_samples]
        freq_res = self.wav_sample_rate / self.fft_n_points
        num_bins = self.fft_n_points / 2
        freq_amp_analysis = []
        for i in range(n_samples):
            analyzed_sample = []
            for j in range(1,num_bins):
                bin = [freq_res*j, magnitudes[i][j]]
                analyzed_sample.append(bin)
            freq_amp_analysis.append(analyzed_sample)
        freq_amp_analysis = [normalize(l) for l in freq_amp_analysis]
        freq_amp_analysis = [loudest_partials(l,n_partials) for l in freq_amp_analysis]
        self.deep_analysis = freq_amp_analysis
    
    def get_modal_data(self, n_modes):
        self.n_loudest_partials(n_modes)
        
        #reduce deep_analysis to the n_modes desired 
        for i in range(len(self.deep_analysis)):  
            self.deep_analysis[i] = loudest_partials(self.deep_analysis[i], n_modes)
        pt = Partial_Tracker(self)
        pt.partial_track()
        pt.create_modal_model()
        self.modal_model = pt.modal_model
        

#---------------------------------------------------------------------
#_Utilities

def fft_to_magnitude(fft_array):
    fft_array = deepcopy(fft_array)
    for i in range(len(fft_array)):
        fft_array[i] = absolute(fft_array[i])
    return fft_array


def normalize(bins):
    maxamp = 0
    for bin in bins:
        if (abs(bin[1]) > maxamp):
            maxamp = abs(bin[1])
    scalar = 1/maxamp
    for bin in bins:
        bin[1] *= scalar
    return bins


def loudest_partials(bins, n):
    amplitudes = []
    amp_dict = {}
    for bin in bins:
        amplitudes.append(bin[1])
        amp_dict[bin[1]] = bin[0]
    amplitudes.sort()
    amplitudes = amplitudes[-n:]
    new_bins = []
    for amp in amplitudes:
        new_bins.append([amp_dict[amp], amp])
    new_bins.reverse()
    return new_bins