#!/usr/bin/env python
# FFT_Analyzer.py - John Burnett & Will Johnson (c)2015
# Class for performing FFT analysis of audio
#
# Usage:
# Initialize instance with wav file
# Call perform_analysis()
# Call stft() for FFT analysis over time

from scipy.fftpack import fft, rfft, irfft, fftfreq
from scipy.io import wavfile
from scipy.signal import get_window
import scipy
import numpy
from copy import deepcopy
from WAV_Reader import WAV_Reader
from partialTracking import Partial_Tracker
from progressbar import *

class FFT_Analyzer:

    def __init__(self, wav_file, n_points=2048):
        self.wav_name = wav_file
        self.wav_data = []
        self.wav_sample_rate = 44100
        self.length_in_seconds = 0
        self.fft_data = []
        self.fft_n_points = n_points
        self.bins = []
        self.stft_analysis = []
        self.modal_model = []
        self.partial_track = []


    def get_length_in_seconds(self):
        self.length_in_seconds = float(len(self.wav_data))/float(self.wav_sample_rate)


    def extract_samples(self):
        """
        Populates self.wav_data using instance of WAV_Reader
        """
        wav_extract = WAV_Reader(self.wav_name)
        wav_extract.toMono()
        self.wav_data = wav_extract.data
        self.wav_sample_rate = wav_extract.sampleRate


    def fft_analysis(self, M, time = .2):
        """
        Populates self.fft_analysis with raw FFT coefficients

        Special thanks to SMS-tools and the ASPMA course - WEJ
        """
        #blackman window
        w = get_window("hann", M)
        w = w / sum(w)
        if (w.size > self.fft_n_points):
            raise ValueError("window size greater than FFT Size")
        sample = int(time*self.wav_sample_rate)
        if (sample+M >= self.wav_data.size or sample <0):
            raise ValueError("time outside sound boundaries")
        x = self.wav_data[sample:sample+M]
        hN = (self.fft_n_points/2)+1
        hM1 = int(math.floor((w.size+1)/2))
        hM2 = int(math.floor(w.size/2))
        fft_buffer = numpy.zeros(self.fft_n_points)
        xw =x*w
        fft_buffer[:hM1] = xw[hM2:]
        fft_buffer[-hM2:] = xw[:hM2]
        X = fft(fft_buffer)
        self.fft_data = X
        #self.fft_data = list(fft(self.wav_data, self.fft_n_points))


    def generate_bins(self):
        """
        Converts FFT coefficients to [freq, amp] bins
        Populates self.bins with bins
        """
        magnitudes = fft_to_magnitude(self.fft_data, self.fft_n_points)
        freq_res = self.wav_sample_rate / self.fft_n_points
        num_bins = self.fft_n_points / 2

        for i in range(1,num_bins):
            self.bins.append([freq_res*i, magnitudes[i]])


    def normalize_amplitudes(self):
        """
        Normalizes amplitudes to values between 0.0 and 1.0
        """
        self.bins = normalize(self.bins)


    def n_loudest_partials(self, n=100):
        """
        Strips self.bins to its n loudest partials

        Args:
            n: number of desired partials
        """
        self.bins = loudest_partials(self.bins, n)


    def perform_analysis(self):
        """
        Extracts samples, performs analysis, normalizes, and strips in series
        """
        self.extract_samples()
        self.get_length_in_seconds()
        self.fft_analysis(1024)
        self.generate_bins()
        self.normalize_amplitudes()
        #self.n_loudest_partials()


    def stft(self, n_samples, n_partials):
        """
        Performs FFT analysis over time

        Args:
            n_samples: number of FFT windows
            n_partials: number of desired partials
        """

        ## 11/18/2015 - will - after restructuring and improving 
        ## fft this is now broken, the main fft method no longer
        ## takes the fft of the whole file, so implementing it
        ## here doesn't work out. 
        ## the partial tracking durations are uniform

        print "Performing stft..."

        split_wav_samples = numpy.array_split(self.wav_data, n_samples)
        split_wav_samples = [list(l) for l in split_wav_samples]
        num_bins = self.fft_n_points / 2
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(split_wav_samples)+n_samples+num_bins).start()
        fft_samples = []
        for i, l in enumerate(split_wav_samples):
            fft_of_sample = fft(l, self.fft_n_points)
            fft_samples.append(fft_of_sample)
            progress.update(i+1)
        magnitudes = [fft_to_magnitude(l, self.fft_n_points) for l in fft_samples]
        freq_res = self.wav_sample_rate / self.fft_n_points
        freq_amp_analysis = []
        for i in range(n_samples):
            analyzed_sample = []
            for j in range(1,num_bins):
                bin = [freq_res*j, magnitudes[i][j]]
                analyzed_sample.append(bin)
                progress.update(j+1)
            freq_amp_analysis.append(analyzed_sample)
            progress.update(i+1)
        #need to use different normalization algorithm, the below looks like
        #it would fuck up natural decays
        #freq_amp_analysis = [normalize(l) for l in freq_amp_analysis]
        maxamp = 0
        for s in freq_amp_analysis:
            for b in s:
                if abs(b[1]) > maxamp:
                    maxamp = abs(b[1])
        scalar = 1/maxamp
        print scalar
        for s in freq_amp_analysis:
            for b in s:
                b[1] *= scalar 
        self.stft_analysis = freq_amp_analysis
        progress.finish()


    def get_partial_track(self):
        """
        Tracks partials of analysis
        """
        pt = Partial_Tracker(self)
        pt.partial_track()
        self.partial_track = pt.partials


    def get_modal_data(self, n_modes):
        """
        Calculates modal data

        Args:
            n_modes: max number of desired modes
        """
        self.n_loudest_partials(n_modes)
        pt = Partial_Tracker(self)
        pt.partial_track()
        self.modal_model = pt.create_modal_model(n_modes)


#---------------------------------------------------------------------
#_Utilities

def fft_to_magnitude(fft_array, N):
    """
    Converts imaginary FFT coefficients to real magnitudes

    Args:
        fft_array: list of FFT coefficients
    Returns:
        converted array
    """
    fft_array = fft_array.copy()
    absX = abs(fft_array[:(N/2)+1])
    absX[absX<numpy.finfo(float).eps] = numpy.finfo(float).eps
    mX = 20 * numpy.log10(absX)
    return mX


def normalize(bins):
    """
    Normalizes amplitudes of bins in window

    Args:
        bins: list of FFT bins
    """
    maxamp = 0
    for bin in bins:
        if (abs(bin[1]) > maxamp):
            maxamp = abs(bin[1])
    scalar = 1/maxamp
    for bin in bins:
        bin[1] *= scalar
    return bins


def scale(data, new_min, new_max):
    old_min = min(data)
    old_max = max(data)
    old_range = old_max - old_min
    new_range = new_max - new_min
    for i in range(len(data)):
        data[i] = (((data[i] - old_min) * new_range) / old_range) + new_min


def loudest_partials(bins, n):
    """
    Strips bin list to n partials

    Args:
        n: number of desired partials
    Returns:
        n loudest partials
    """
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
