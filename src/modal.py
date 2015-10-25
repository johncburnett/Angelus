#!/usr/bin/env python

from FFT_Analyzer import FFT_Analyzer
from writeRObU import writeRObU
from Synthesizer import Synthesizer
import sys

def main():
    # infile = raw_input("Enter input audio file path: ")
    # outfile = raw_input("Enter output analysis file path: ")
    fname = sys.argv[1]
    title = parse_fname(fname)
    infile = "../audio/" + fname
    outfile = "../build/" + title + ".ro"
    analysis = FFT_Analyzer(infile)
    analysis.perform_analysis()
    analysis.perform_deep_analysis(20,1000)
    analysis.get_modal_data(30)
    out = writeRObU(outfile, analysis.modal_model)
    out.write()

    synth = Synthesizer(analysis, title)
    synth.write_wav()


def parse_fname(fname):
    s = ""
    for l in fname:
        if l != '.': s += l
        else: return s


main()
