#!/usr/bin/env python

from scipy import array
from scipy.fftpack import ifft
from scipy.io import wavfile
from WAV_Reader import WAV_Reader
from math import sin, pi
from progressbar import ProgressBar, Percentage, Bar

class Synthesizer:

    def __init__(self, analysis, title):
        self.wav_name = title
        self.original_wav = analysis.wav_data
        self.fft_data = analysis.fft_data
        self.sample_rate =analysis.wav_sample_rate
        self.bins = analysis.bins
        self.num_samples = len(analysis.wav_data)
        self.frate = 11025.0


    def write_wav(self):
        print("Performing Resynthesis...")
        progress = ProgressBar(
                widgets=[Percentage(), Bar()],
                maxval=self.num_samples
                ).start()


        sines = []
        for i in range(len(self.bins)):
            data = [sin(2 * pi * self.bins[i][0] * (x / self.frate))
                    for x in range(self.num_samples)]
            for s in data:
                s = s * self.bins[i][1]
            sines.append(data)
        samples = []
        for i in range(len(sines[0])):
            s = 0
            for j in range(len(sines)):
                s += sines[j][i]
            samples.append(s)
            progress.update(i+1)
        samples = scale(samples, -1.0, 1.0)

        wavfile.write("../synthesis/" + self.wav_name + "_resynth.wav", self.sample_rate, array(samples))
        progress.finish()


    def write_residual(self):
        ifft_data = perform_ifft(self.fft_data, self.original_wav)
        resynthesis = scale(ifft_data[0], -1, 1)
        noise = scale(ifft_data[1], -1, 1)
        wavfile.write("../synthesis/" + self.wav_name + "_noise.wav", self.sample_rate, noise)


#---------------------------------------------------------------------
#_Utilities

def perform_ifft(fft_data, wav_data):
    ifft_data = list(ifft(fft_data))
    noise = []
    for i in range(len(ifft_data)):
        noise.append(wav_data[i] - ifft_data[i])
    return (ifft_data, noise)


def scale(data, new_min, new_max):
    old_min = min(data)
    old_max = max(data)
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_data = []
    for i in range(len(data)):
        new_data.append( (((data[i] - old_min) * new_range) / old_range) + new_min )
    return new_data
