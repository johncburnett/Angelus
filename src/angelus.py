#!/usr/bin/env python
# angelus.py - John Burnett & Will Johnson (c)2015
# 
# Angelus does the following:
# -FFT analysis
# -Partial tracking
# -Modal analysis
# -Resynthesis
# 
# Angelus will eventually do the following:
# -FFT Analysis -> Notation
# -Modal Analysis -> 3D mesh (and reverse?)

from FFT_Analyzer import FFT_Analyzer
from writeRObU import writeRObU
from Synthesizer import Synthesizer
import sys

def main():
    fname = sys.argv[1]
    title = parse_fname(fname)
    infile = "../audio/" + fname
    outfile = "../build/" + title + ".ro"
    analysis = FFT_Analyzer(infile)
    analysis.perform_analysis()
    analysis.stft(20)
    analysis.get_modal_data(30)
    out = writeRObU(outfile, analysis.modal_model)
    out.write()

    synth = Synthesizer(analysis, title)
    synth.write_wav()
    #synth.write_residual()


def parse_fname(fname):
    s = ""
    for l in fname:
        if l != '.': s += l
        else: return s


main()
