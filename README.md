## Audio Spectrum Analyzer
This software is an easy-to-use, lightweight and real-time audio signal analyzer that shows time-domain raw signal and its frequency spectrum.

**Note:** This code has been developed as a part of research project. Currently, I have no time to work on bugs or any improvements. Please feel free to report any issues/bugs/suggestions.

![screenshot](/assets/example.png)

## Key Features

* Real-time processing audio signal and displaying the its FFT. 
  - Instantly see the filtered and/or windowed audio signal.
* Bandpass and highpass filtering.
* Various time-domain windowing functions.
* Cross platform
  - Tested on Windows and MacOS.

## Requirements

[![PyQt5](https://img.shields.io/badge/PyQt5-%3E5.15.4-C00)](https://pypi.org/project/PyQt5/)

[![Matplotlib](https://img.shields.io/badge/Matplotlib-%3E3.4.2-yellow)](https://matplotlib.org/)

[![SciPy](https://img.shields.io/badge/SciPy-%3E1.6-orange)](https://scipy.org/)

[![NumPy](https://img.shields.io/badge/NumPy-%3E1.20.3-blueviolet)](https://numpy.org/)

[![PyAudio](https://img.shields.io/badge/PyAudio-%3E0.2.11-red)](https://pypi.org/project/PyAudio/)

[![PyQtGraph](https://img.shields.io/badge/PyQtGraph-%3E0.2.1-brightgreen)](https://www.pyqtgraph.org/)

[![Progress](https://img.shields.io/badge/Progress-%3E1.6-blue)](https://pypi.org/project/progress/)

[![pyperclip](https://img.shields.io/badge/pyperclip-%3E1.8.2-critical)](https://pypi.org/project/pyperclip/)

## Usage

**MacOS:** In MacOS, the audio analyzer can simply be launched with a terminal as follows:
```
clear & sh run.sh -n -q -r 48000
```

There are several different command-line arguments available:
* ```-q```, ```--quiet``` **Quiet:** No messages are shown in the command line.
* ```-v```, ```--verbose``` **Verbose:** Verbose output shows important information on the command line.
* ```-n```, ```--no_log_save``` **No Log Save:** Do not save a log file.
* ```-r```, ```--rate``` **Rate:** The rate at which the sampling is performed. The default is 44.1 kHz and 48 kHz for Windows and MacOS, respectively.
* ```-l```, ```--log_filename``` **Log Filename:** User-defined log file name. Should not be used together with the argument ```--no_log_save```.

An example usage would be (although using ```clear``` is optional):
```
clear & sh run.sh -n -q -r 48000
```

**Windows:** Windows users can go into the ```src/``` directory and directly run the Python code using the following command to PowerShell in order to launch the audio analyzer:
```
cd src
python run.py
```

## Audio Analyzer Help
This section can be found inside the program under the menubar Help > Audio Analyzer Help. The top section of the Audio Analyzer is divided into two sections: Waveform and Spectrum. Waveform shows the instantaneous audio signal in time-domain. Spectrum shows the FFT of the real-time audio signal that is the spectrum of the wave in frequency-domain. Signal amplitude is shown in Waveform while Spectrum shows the frequency components of the real-time audio signal captured by the default microphone of the operating system. Currently, there is no option available for selecting the microphone. The program will automatically detect the microphone, and if there is no microphone detected, there will be an error message displayed on the command line such as: ```No audio input device is found.```

The bottom section comprises of options that can be set in order to digitally process the real-time audio signal in different ways. One can play with the options to observe changes in Spectrum where the filtering or windowing results can be seen more explicitly.

The audio analyzer has various functionalities that are described as follows:

**1. Filtering:** It is enabled in default. There are two types available: highpass and bandpass where the former filters the low frequency components while passing the high frequency components, and the latter only passes certain band of frequencies. These frequencies are defined with Cutoff Frequency option that can be set by the user. It is suggested to use Bandpass Butterworth filter with a filter order of 3 or 5.

**2. Windowing:** The usage of windowing is optional. The windowing in time-domain can however be very useful in suppressing the residual frequency components that may emerge far away from the frequency band of interest. For example, user can be interested in analyzing low frequencies, say around a couple hundreds of Hz, while noise-like spectral components can arise around a few MHz which in turn can be quite effectively smoothed out using windowing. It is suggested to use Hann window; however, the effect of other window functions can be observed and therefore used.

Comparison of different windowing functions:

| **Window**<br>**Function** | **Spectral**<br>**Leakage** | **Amplitude**<br>**Accuracy** | **Frequency**<br>**Resolution** |
| :---: | :---: | :---: | :---: |
| Blackman | Best | Good | Fair |
| Flattop | Good | Best | Poor |
| Rectangle (none) | Poor | Poor | Best |
| Hann | Good | Fair | Good |
| Hamming | Fair | Fair | Good |
| Kaiser | Good | Good | Fair |

**3. Status Bar:** Status bar will show the changes made in Filtering or Windowing options.

**4. Frequency Status Bar:** It is the status bar on the right that shows the frequency point at which the highest peak occured in the Spectrum plot.

**5. Response Buttons:** Filter and window function frequency responses can be plotted. It is a nice way to visualize frequency response of filters and window functions as the information regarding the passband and stopband responses can be used to tweak the cutoff frequencies so that the user can attain an ideal output.

**6. Snapshot:** The Snapshot button can take instantaneous output of the Waveform and Spectrum plots. The two resulting images obtained for time- and frequency-domain responses are recorded in the same directory of the program file.