#!/usr/bin/env python
# writeRObU.py - John Burnett & Will Johnson (c)2015
# File IO for Angelus Project
#
# Usage:
# Initialize instance 
# Call writeRObU() with filename (with extension) and modal data from partial tracker

class writeRObU:

    def __init__(self, filepath, data):
        self.filepath = filepath
        self.data = data

    def write(self):
        fileout = open(self.filepath, "w")
        fileout.write("nactive_freq:\n")
        fileout.write(str(len(self.data))+"\n")
        fileout.write("frequencies:\n")
        for mode in self.data:
            fileout.write(str(mode[0])+"\n")
        fileout.write("dampings:\n")
        for mode in self.data:
            fileout.write(str(1/mode[1])+"\n")
        fileout.write("amplitudes[point][freq]:\n")
        for mode in self.data:
            fileout.write(str(mode[2])+"\n")
        fileout.write("END\n")
        
    
        
        
