# Angelus

A set of audio analysis tools: analyzing spectral data of .wav files. 

###Features:

* FFT Analysis 
* Partial Tracking 
* Modal Extraction
* Resynthesis

###Usage:

To use Angelus, place the WAV file(s) you would like to analyze into the `audio` directory and run:
```shell
./angelus file1.wav file2.wav file3.wav
```
or analyze all files:
```shell
./angelus -a
```

The analysis and resynthesis of your file(s) will be written to the `build` and `synthesis` directories.

###Dependencies:

* scipy
* progressbar
