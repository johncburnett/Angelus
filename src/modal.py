from FFT_Analyzer import FFT_Analyzer

def main():
    analysis = FFT_Analyzer('test.wav')
    analysis.perform_analysis()
    print analysis.bins
    toRObU(analysis)
    
def toRObU(analysis, outfile="test.ro"):
    fileout = open(outfile, "w")
    fileout.write("nactive_freq:\n")
    fileout.write(str(len(analysis.bins))+"\n")
    fileout.write("frequencies:\n")
    for bin in analysis.bins:
        fileout.write(str(bin[0])+"\n")
    fileout.write("dampings:\n")
    for bin in analysis.bins:
        # don't have this yet
        fileout.write("error\n")
    fileout.write("amplitudes[point][freq]:\n")
    for bin in analysis.bins:
        fileout.write(str(bin[1])+"\n")
    fileout.write("END\n")
        

main()