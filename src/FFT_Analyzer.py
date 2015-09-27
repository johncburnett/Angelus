#!/usr/bin/env python

from scipy.fftpack import fft, ifft
from numpy import absolute
from copy import deepcopy
from WAV_Reader import WAV_Reader

class FFT_Analyzer:

    def __init__(self, wav_file, n_points=8192):
        self.wav_name = wav_file
        self.wav_data = []
        self.wav_sample_rate = 44100
        self.fft_data = []
        self.fft_n_points = n_points
        self.bins = []


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
        maxamp = 0
        for bin in self.bins:
            if (abs(bin[1]) > maxamp):
                maxamp = abs(bin[1])

        scalar = 1/maxamp
        for bin in self.bins:
            bin[1] *= scalar
            
    def n_loudest_partials(self, n=10):
        amplitudes = []
        amp_dict = {}
        for bin in self.bins:
            amplitudes.append(bin[1])
            amp_dict[bin[1]] = bin[0]
        amplitudes.sort()
        amplitudes = amplitudes[-n:]
        new_bins = []
        for amp in amplitudes:
            new_bins.append([amp_dict[amp], amp])
        self.bins = new_bins
        self.bins.reverse()
        

    def perform_analysis(self):
        self.extract_samples()
        self.fft_analysis()
        self.generate_bins()
        self.normalize_amplitudes()
        self.n_loudest_partials()
        

    #---------------------------------------------------------------------
    #_Utilities

def fft_to_magnitude(fft_array):
    fft_array = deepcopy(fft_array)
    for i in range(len(fft_array)):
        fft_array[i] = absolute(fft_array[i])
    return fft_array