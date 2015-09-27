from scipy.fftpack import fft, ifft
from numpy import absolute
from WAV_Reader import WAV_Reader

class FFT_Analyzer:

	def __init__(self, wav_file, n_points=256):
		self.wav_name = ''
		self.wav_data = []
		self.wav_sample_rate = 44100
		self.fft_data = []
		self.fft_n_points = 256
		self.bins = []


	def extract_samples(self):
		wav_extract = WAV_Reader('ex.wav')
		wav_extract.extract_samples('ex.wav')
		wav_extract.toMono()
		self.wav_data = wav_extract.data
		self.wav_sample_rate = wav_extract.sampleRate


	def fft_analysis(self):
		self.fft_data = fft(self.wav_data, self.fft_n_points)


	def generate_bins(self):
		magnitudes = fft_to_magnitude(self.fft_data)
		freq_res = self.wav_sample_rate / fft_n_points
		num_bins = self.fft_n_points / 2

		for i in range(1,num_bins):
			self.bins[i].append([freq_res*i, magnitudes[i]])


	def perform_analysis(self):
		self.extract_samples()
		self.fft_analysis()
		self.generate_bins()


	#---------------------------------------------------------------------
	#_Utilities

	def fft_to_magnitude(fft_array):
		for x in fft_array:
			x = numpy,absolute(x)
		return fft_array