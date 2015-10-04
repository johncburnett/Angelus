#!/usr/bin/env python

from FFT_Analyzer import FFT_Analyzer
from writeRObU import writeRObU

def main():
    infile = raw_input("Enter input audio file path: ")
    outfile = raw_input("Enter output analysis file path: ")
    analysis = FFT_Analyzer(infile)
    analysis.perform_analysis()
    analysis.perform_deep_analysis(40,1000)
    analysis.get_modal_data(30)
    out = writeRObU(outfile, analysis.modal_model)
    out.write()
    
main()