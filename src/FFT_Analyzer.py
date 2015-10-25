#!/usr/bin/env python
# FFT_Analyzer.py - John Burnett & Will Johnson (c)2015
# Class for performing FFT analysis of audio
#
# Usage:
# Initialize instance with wav file
# Call perform_analysis()
# Call perform deep_analysis() for FFT analysis over time

from scipy.fftpack import fft, ifft, rfft, irfft, fftfreq
from scipy.io import wavfile
import scipy
from numpy import absolute
from numpy import array_split
from copy import deepcopy
from WAV_Reader import WAV_Reader
from partialTracking import Partial_Tracker
from progressbar import *

class FFT_Analyzer:
    """

    THINGS TO DO:

    IFFT

    RESIDUAL EXTRACTION METHOD: TAKES IN WAV FILE AND REMOVES THE PARTIAL CONTENT, RETURNING AN AUDIOFILE OF JUST THE 'NOISE' OF THE SOUND


    """
    def __init__(self, wav_file, n_points=8192*2):
        self.wav_name = wav_file
        self.wav_data = []
        self.wav_sample_rate = 44100
        self.length_in_seconds = 0
        self.fft_data = []
        self.fft_n_points = n_points
        self.bins = []
        self.deep_analysis = []
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


    def fft_analysis(self):
        """
        Populates self.fft_analysis with raw FFT coefficients
        """
        self.fft_data = list(fft(self.wav_data, self.fft_n_points))


    def generate_bins(self):
        """
        Converts FFT coefficients to [freq, amp] bins
        Populates self.bins with bins
        """
        magnitudes = fft_to_magnitude(self.fft_data)
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
        self.fft_analysis()
        self.generate_bins()
        self.normalize_amplitudes()
        self.n_loudest_partials()


    def perform_deep_analysis(self, n_samples, n_partials):
        """
        Performs FFT analysis over time

        Args:
            n_samples: number of FFT windows
            n_partials: number of desired partials
        """

        print "Performing Deep Analysis..."

        split_wav_samples = array_split(self.wav_data, n_samples)
        split_wav_samples = [list(l) for l in split_wav_samples]
        num_bins = self.fft_n_points / 2
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(split_wav_samples)+n_samples+num_bins).start()
        fft_samples = []
        for i, l in enumerate(split_wav_samples):
            fft_of_sample = self.fft_data = list(fft(l, self.fft_n_points))
            fft_samples.append(fft_of_sample)
            progress.update(i+1)
        magnitudes = [fft_to_magnitude(l) for l in fft_samples]
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
        freq_amp_analysis = [normalize(l) for l in freq_amp_analysis]
        #freq_amp_analysis = [loudest_partials(l,n_partials) for l in freq_amp_analysis]
        self.deep_analysis = freq_amp_analysis
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

def fft_to_magnitude(fft_array):
    """
    Converts imaginary FFT coefficients to real magnitudes

    Args:
        fft_array: list of FFT coefficients
    Returns:
        converted array
    """
    fft_array = deepcopy(fft_array)
    for i in range(len(fft_array)):
        fft_array[i] = absolute(fft_array[i])
    return fft_array


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
