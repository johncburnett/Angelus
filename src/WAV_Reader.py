#!/usr/bin/env python

import scipy.io.wavfile

class WAV_Reader:
    
    def __init__ (self, filename):
        self.scipyDump = self.extract_samples(filename)
        self.filename = filename
        self.data = self.scipyDump[1]
        self.sampleRate = self.scipyDump[0]
        self.channels = len(self.scipyDump[1][0])
        
        print "filename: "+str(self.filename)
        print "sample rate: "+str(self.sampleRate)
        print "channels: "+str(self.channels)
        
    def extract_samples(self, filename):
        return scipy.io.wavfile.read(filename)