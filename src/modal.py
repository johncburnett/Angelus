#!/usr/bin/env python

from FFT_Analyzer import FFT_Analyzer
from writeRObU import writeRObU
from Synthesizer import Synthesizer

def main():
    # infile = raw_input("Enter input audio file path: ")
    # outfile = raw_input("Enter output analysis file path: ")
    infile = "../audio/test.wav"
    outfile = "../build/test.ro"
    analysis = FFT_Analyzer(infile)
    analysis.perform_analysis()
    analysis.perform_deep_analysis(20,1000)
    analysis.get_modal_data(30)
    out = writeRObU(outfile, analysis.modal_model)
    out.write()

    synth = Synthesizer(analysis)
    synth.write_wav()

main()
