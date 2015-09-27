from scipy.fftpack import fft, ifft
from numpy import absolute
from copy import deepcopy
from WAV_Reader import WAV_Reader

class FFT_Analyzer:

	def __init__(self, wav_file, n_points=256):
		self.wav_name = wav_file
		self.wav_data = []
		self.wav_sample_rate = 44100
		self.fft_data = []
		self.fft_n_points = 256
		self.bins = []


	def extract_samples(self):
		wav_extract = WAV_Reader(self.wav_name)
		wav_extract.toMono()
		self.wav_data = wav_extract.data
		self.wav_sample_rate = wav_extract.sampleRate


	def fft_analysis(self):
		self.fft_data = list(fft(self.wav_data, self.fft_n_points))



	def generate_bins(self):
		magnitudes = fft_to_magnitude(self.fft_data)
		freq_res = self.wav_sample_rate / self.fft_n_points
		num_bins = self.fft_n_points / 2

		for i in range(1,len(magnitudes)):
			self.bins.append([freq_res*i, magnitudes[i]])


	def perform_analysis(self):
		self.extract_samples()
		self.fft_analysis()
		self.generate_bins()


	#---------------------------------------------------------------------
	#_Utilities

def fft_to_magnitude(fft_array):
	fft_array = deepcopy(fft_array)
	for i in range(len(fft_array)):
		fft_array[i] = absolute(fft_array[i])
	return fft_array