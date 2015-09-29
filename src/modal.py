#!/usr/bin/env python

from FFT_Analyzer import FFT_Analyzer

def main():
    analysis = FFT_Analyzer('../audio/test.wav')
    analysis.perform_analysis()
    analysis.perform_deep_analysis(10,1000)
    #analysis.get_partial_track()
    analysis.get_modal_data(10)
    toRObU(analysis)
    
def toRObU(analysis, outfile="../build/test.ro"):
    fileout = open(outfile, "w")
    fileout.write("nactive_freq:\n")
    fileout.write(str(len(analysis.modal_model))+"\n")
    fileout.write("frequencies:\n")
    for mode in analysis.modal_model:
        fileout.write(str(mode[0])+"\n")
    fileout.write("dampings:\n")
    for mode in analysis.modal_model:
        fileout.write(str(1/mode[1])+"\n")
    fileout.write("amplitudes[point][freq]:\n")
    for mode in analysis.modal_model:
        fileout.write(str(mode[2])+"\n")
    fileout.write("END\n")
        

main()