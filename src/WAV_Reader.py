#!/usr/bin/env python
# WAV_Reader.py - John Burnett & Will Johnson (c)2015
# Class for reading a .wav file to an array
#
# Usage:
# Initialize instance with file path
# Call toMono() to convert a file of any number of channels to mono
# Call norm() to normalize a mono file

import scipy.io.wavfile
import numpy

class WAV_Reader:
    
    #documentation! 
    
    def __init__ (self, filename):
        self.filename = filename
        self.scipyDump = scipy.io.wavfile.read(self.filename)
        self.data = self.scipyDump[1]
        self.sampleRate = self.scipyDump[0]
        self.channels = self.get_n_channels()
        
        print "filename: "+str(self.filename)
        print "sample rate: "+str(self.sampleRate)
        print "channels: "+str(self.channels)
        
    def toMono(self):
        if self.channels > 1:
            temp = 0
            mono_data = []
            for s in self.data:
                for c in s:
                    temp += c
                temp = temp/self.channels
                mono_data.append(temp)
            mono_data = self.norm(mono_data)
            self.data = mono_data
        else:
            return
    
    def get_n_channels(self):
        if type(self.scipyDump[1][0]) == numpy.int16:
            self.channels = 1
        else:
            self.channels = len(self.scipyDump[1][0])
            
        
    def norm(self, data):
        maxSample = 0
        scalar = 0
        for s in data:
            if abs(s) > maxSample:
                maxSample = s
        scalar = 1/maxSample
        for s in data:
             s *= scalar
        return data