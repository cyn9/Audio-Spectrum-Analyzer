## Audio Spectrum Analyzer
This software is an easy-to-use, lightweight and real-time audio signal analyzer that shows time-domain raw signal and its frequency spectrum.

![screenshot](/assets/example.png)

## Key Features

* Real-time processing audio signal and displaying the its FFT. 
  - Instantly see the filtered and/or windowed audio signal.
* Bandpass and highpass filtering.
* Various time-domain windowing functions.
* Cross platform
  - Tested on Windows and MacOS.

## Usage

In MacOS, the audio analyzer can simply be launched with a terminal as follows:
```
clear & sh run.sh -n -q -r 48000
```

There are several different command-line arguments available:
* [-q, --quiet] Quiet: No messages are shown in the command line.
* [-v, --verbose] Verbose: Verbose output shows important information on the command line.
* [-n, --no_log_save] No-Log-Save: Do not save a log file.
* [-r, --rate] Rate: The rate at which the sampling is performed. The default is 44.1 kHz and 48 kHz for Windows and MacOS, respectively.
* [-l, --log_filename] Log-Filename: User-defined log file name. Should not be used together with the argument --no_log_save.
