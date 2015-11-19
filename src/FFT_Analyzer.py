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
import math
from copy import deepcopy
from WAV_Reader import WAV_Reader
from partialTracking import Partial_Tracker
from progressbar import *

class FFT_Analyzer:

    def __init__(self, wav_file, N=1024):
        self.wav_name = wav_file
        self.wav_data = []
        self.wav_sample_rate = 44100
        self.length_in_seconds = 0
        self.N = N
        self.M = 511
        self.window = self.obtain_window()
        self.fft_data = []
        self.hN = (self.N/2)+1
        self.hM1 = int(math.floor((self.window.size+1)/2))                  
        self.hM2 = int(math.floor(self.window.size/2)) 
        self.mX = []
        self.pX = []
        self.stft_analysis = []
        self.modal_model = []
        self.partial_track = []


    def obtain_window(self):
        w = get_window("blackman", self.M)
        w = w/ sum(w)
        return w


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


    def perform_fft(self, x):
        X = self.fft_analysis(x)
        mX = self.generate_mX(X)
        return mX


    def fft_analysis(self, x, time_offset=1):
        """
        Populates self.fft_analysis with raw FFT coefficients

        Special thanks to SMS-tools and the ASPMA course - WEJ
        """
        if (self.window.size > self.N):
            raise ValueError("window size greater than FFT Size")
        sample = time_offset
        if (sample+self.M >= len(self.wav_data) or sample < 0):
            raise ValueError("time outside sound boundaries")
        x = self.wav_data[sample:sample+self.M]
        fft_buffer = numpy.zeros(self.N)
        xw =x*self.window
        fft_buffer[:self.hM1] = xw[self.hM2:]
        fft_buffer[-self.hM2:] = xw[:self.hM2]
        X = fft(fft_buffer)
        return x


    def generate_mX(self, X):
        """
        Converts FFT coefficients to [freq, amp] bins

            args: fft complex coefficients
        """
        magnitudes = fft_to_magnitude(X, self.N)
        freq_step = self.wav_sample_rate / self.N
        mX = []
        for i in range(len(magnitudes)):
            mX.append([freq_step*i, magnitudes[i]])
        return mX


    def normalize_amplitudes(self):
        """
        Normalizes amplitudes to values between 0.0 and 1.0
        """
        self.mX = normalize(self.mX)


    ## create normalize stft method??

    def n_loudest_partials(self, n=100):
        """
        Strips self.mX to its n loudest partials

        Args:
            n: number of desired partials
        """
        self.mX = loudest_partials(self.mX, n)


    def perform_analysis(self):
        """
        Extracts samples, performs analysis, normalizes, and strips in series
        """
        self.extract_samples()
        self.get_length_in_seconds()
        self.mX = self.perform_fft(self.wav_data)
        self.normalize_amplitudes()


    def stft(self, H=512):
        """
        Performs FFT analysis over time

        Args:
            H: hop size
        """

        print "Performing STFT..."
        x = self.wav_data
        x = numpy.append(numpy.zeros(self.hM2),x)  
        x = numpy.append(x, numpy.zeros(self.hM1))
        M = self.window.size
        pin = self.hM1
        pend = x.size-self.hM1
        progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=(pend+H)).start()
        xmX = []
        while pin<=pend:                                  # while sound pointer is smaller than last sample      
            progress.update(pin)
            x1 = x[pin-self.hM1:pin+self.hM2]             # select one frame of inumpyut sound
            mX = self.perform_fft(x1)                      # compute dft
            if pin == self.hM1:                                # if first frame create output arrays
                xmX = [mX]
                #xpX = numpy.array([pX])
            else:                                         # append output to existing array 
                xmX.append(mX)
                #xpX = numpy.vstack((xpX,numpy.array([pX])))
            pin += H                                      # advance sound pointer
        ## normalization
        maxamp = 0
        for a in xmX:
            for b in a:
                if abs(b[1]) > maxamp:
                    maxamp = abs(float(b[1]))
        scalar = 1/maxamp
        for a in xmX:
            for b in a:
                ## here's where i'm fudging a bigger issue with negative magnitudes
                b[1] *= -scalar
        self.stft_analysis = xmX
        progress.finish()
        self.debug_print_to_file()


    def debug_print_to_file(self):
        fileout = open("../debug.txt", "w")
        fileout.write(str(self.stft_analysis))


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

def fft_to_magnitude(X, N):
    """
    Converts imaginary FFT coefficients to real magnitudes

    Args:
        X: list of FFT coefficients
        N: fft size
    Returns:
        converted array
    """
    X = numpy.array(X)
    absX = abs(X[:(N/2)+1])
    absX[absX<numpy.finfo(float).eps] = numpy.finfo(float).eps
    mX = 20 * numpy.log10(absX)
    return list(mX)


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
