from FFT_Analyzer import FFT_Analyzer

def main():
	analysis = FFT_Analyzer('test.wav')
	analysis.perform_analysis()
	print analysis.bins

main()