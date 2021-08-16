'''
Following features will be implemented:
(1) Dynamic range compression
(2) Limiter
(3) Noise reduction
(4) Timestamp in status window and saving log files.
'''

from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QApplication

from scipy.fftpack import fft
from scipy.fftpack import fftshift
from scipy.signal import lfilter
from scipy.signal import freqz

from tkinter import TclError
from datetime import datetime

from HelpWindow import HelpWindow
from Filtering import *
from Windowing import *
from DeviceInfo import *
from Log import *

import platform
import numpy as np
import pyqtgraph as pg
import matplotlib as mpl
import matplotlib.pyplot as plt
import pyaudio
import struct
import sys

class MainWindow(QtWidgets.QMainWindow):
    # def __init__(self, *args, **kwargs):
    def __init__(self, cmd_args, *args, **kwargs):
        # Platform check for MacOS
        # Somehow there is a problem with the Tk backend.
        self.opSystem = platform.system()
        if self.opSystem == "Darwin":
            mpl.use('Qt5Agg')

        self.arg_quiet   = cmd_args[0]
        self.arg_verbose = cmd_args[1]
        self.arg_nologs  = cmd_args[2]

        # print(f"Arguments passed:")
        # print(f"Quiet   : {self.arg_quiet}")
        # print(f"Verbose : {self.arg_verbose}")
        # print(f"No Logs : {self.arg_nologs}")

        # Some constants
        TD_MIN_X_RANGE = 0
        TD_MAX_X_RANGE = 2**12
        TD_WF_MIN_YVAL = -16000
        TD_WF_MAX_YVAL = 16000
        TD_WF_YMIN = -2**14
        TD_WF_YMAX = 2**14

        # Screen width and height properties overriding
        # QtDesigner values
        SCR_WIDTH = 908
        SCR_HEIGHT = 790

        super(MainWindow, self).__init__(*args, **kwargs)
        pg.setConfigOptions(antialias = True)

        # Load the UI Page
        uic.loadUi("/Users/ciyan/Documents/Audio-Spectrum-Analyzer/ui/MainWindow.ui", self)
        self.setFixedSize(SCR_WIDTH, SCR_HEIGHT)

        # Exit app menu item onClick event
        self.action_ExitProgram.triggered.connect(self.exitMenuButtonOnClick)

        # About app menu item onClick event
        self.action_About.triggered.connect(self.showAbout)

        # Help app menu item onClick event
        self.action_Help.triggered.connect(self.openWindow2)

        # Remove IIR peak filter item because 'Highpass' option is default.
        self.box_Approx.removeItem(self.box_Approx.findText('IIR Peak'))

        # Default Windowing is disabled. Disable some properties.
        self.chkBox_windowEn.setChecked(False)
        self.lbl_Window.setEnabled(False)
        self.box_Window.setEnabled(False)
        self.btn_WindowResponse.setEnabled(False)

        # Filter enable/disable checkbox properties:
        self.chkBox_filterEn.stateChanged.connect(self.updateFilterStatus)

        # Window function enable/disable checkbox properties:
        self.chkBox_windowEn.stateChanged.connect(self.updateWindowStatus)
        
        # Filter type combobox onSelect event
        self.box_FilterType.activated.connect(self.showBoxFilterTypeCurrentText)
        
        # Window type combobox onSelect event
        self.box_Window.activated.connect(self.showWindowCurrentText)

        # Filter approximation combobox onSelect event
        self.box_Approx.activated.connect(self.showApproxCurrentText)

        # Filter order combobox onSelect event
        self.box_FilterOrder.activated.connect(self.showBoxFilterOrderCurrentText)

        # Default visibility for higher cutoff freq. options
        self.lbl_Cutoff_2.setVisible(False)
        self.txt_Cutoff_2.setVisible(False)

        # Button onClick event for the program termination
        self.btn_Exit.clicked.connect(self.exitProgram)

        # Button onClick event for snapshot
        self.btn_Snapshot.clicked.connect(self.snapshot)

        # Button onClick event for show filter response
        self.btn_FilterResponse.clicked.connect(self.plotFilterResponse)

        # Button onClick event for show window response
        self.btn_WindowResponse.clicked.connect(self.plotWindowResponse)

        # Button onClick event for clear
        self.btn_Clear.clicked.connect(self.clearStatusPane)

        # Traces dictionary as storing plot data names
        self.traces = dict()

        # Graph widget properties
        self.graphWidget_TimeDomain.setLabels(title = '<b><font face="Arial" style="color:white">WAVEFORM</font></b>')
        self.graphWidget_FreqDomain.setLabels(title = '<b><font face="Arial" style="color:white">SPECTRUM</font></b>')

        self.graphWidget_TimeDomain.setLimits(xMin = 0,
                                              xMax = TD_MAX_X_RANGE,
                                              yMin = TD_WF_YMIN,
                                              yMax = TD_WF_YMAX)

        self.graphWidget_TimeDomain.setXRange(min = TD_MIN_X_RANGE,
                                              max = TD_MAX_X_RANGE,
                                              padding = 0.5,
                                              update = True)

        self.graphWidget_TimeDomain.setYRange(min = TD_WF_MIN_YVAL,
                                              max = TD_WF_MAX_YVAL,
                                              padding = 0.5,
                                              update = True)

        self.pyGraphFont = QtGui.QFont("Arial")
        self.pyGraphFont.setPixelSize(14)
        self.pyGraphFont.setBold(True)

        self.graphWidget_TimeDomain.getAxis("bottom").setStyle(tickFont = self.pyGraphFont)
        self.graphWidget_TimeDomain.getAxis("left").setStyle(tickFont = self.pyGraphFont)
        self.graphWidget_FreqDomain.getAxis("bottom").setStyle(tickFont = self.pyGraphFont)
        self.graphWidget_FreqDomain.getAxis("left").setStyle(tickFont = self.pyGraphFont)

        td_wf_xticks = [0, 2048, 4096]
        td_wf_yticks = [-16000, 0, 16000]
        td_wf_xaxis = self.graphWidget_TimeDomain.getAxis('bottom')
        td_wf_yaxis = self.graphWidget_TimeDomain.getAxis('left')
        td_wf_xaxis.setTicks([[(v, str(v)) for v in td_wf_xticks]])
        td_wf_yaxis.setTicks([[(v, str(v)) for v in td_wf_yticks]])
        
        self.graphWidget_FreqDomain.setYRange(min = -4, 
                                              max = 2, 
                                              padding = 0.5,
                                              update = True)

        self.graphWidget_TimeDomain.setMouseEnabled(x = False, y = False)
        self.graphWidget_FreqDomain.setMouseEnabled(x = False, y = False)

        # PyAudio object initialization
        self.FORMAT   = pyaudio.paInt16
        self.CHANNELS = 1
        self.CHUNK = 1024 * 2

        # Note: Some Mac systems have sound cards having a sampling
        # rate of 48 kHz.
        if self.opSystem == "Darwin":
            self.RATE = 48000
        else:
            self.RATE = 44100

        self.p = pyaudio.PyAudio()

        # Get audio device and PyAudio related info
        getDeviceInfo(self.txt_Status, self.p)

        self.chosen_device_index = -1
        for x in range(0, self.p.get_device_count()):
            self.info = self.p.get_device_info_by_index(x)

            if self.info["name"] == "pulse":
                self.chosen_device_index = self.info["index"]
                print(f"Chosen index: {self.chosen_device_index}")

        # Try to start streaming the audio input
        try:
            self.stream = self.p.open(
                format             = self.FORMAT,
                channels           = self.CHANNELS,
                rate               = self.RATE,
                input_device_index = self.chosen_device_index,
                input              = True,
                output             = False,
                frames_per_buffer  = self.CHUNK
            )
        except OSError:
            print("No audio input device is found.")
            sys.exit()
            # Might want to change this from exit() to wait
            # for user input.

        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.f = np.linspace(0, int(self.RATE / 2), int(self.CHUNK / 2))


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


    def setPlotData(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)

        else:
            if name == 'waveform':
                self.traces[name] = self.graphWidget_TimeDomain.plot(pen = pg.mkPen('r', width = 5))
                self.graphWidget_TimeDomain.setXRange(min = 0,
                                                      max = 2 * self.CHUNK,
                                                      padding = 0.5,
                                                      update = True)
                self.graphWidget_TimeDomain.setYRange(min = -16000, 
                                                      max = 16000,
                                                      padding = 0.5,
                                                      update = True)
                                                      
            if name == 'spectrum':
                self.traces[name] = self.graphWidget_FreqDomain.plot(pen = pg.mkPen('r', width = 5))
                self.graphWidget_FreqDomain.setLogMode(x = True, y = True)
                self.graphWidget_FreqDomain.setXRange(min = np.log10(20), 
                                                      max = np.log10(self.RATE / 2), 
                                                      padding = 0.1,
                                                      update = True)
                self.graphWidget_FreqDomain.setYRange(min = -4,
                                                      max = 2, 
                                                      padding = 0.1,
                                                      update = True)


    # Pass the data through the high pass filter
    def filterHighpass(self, data, f_cutoff, fs, approx, order = 5):
        if approx == 'Butterworth':
            b, a = designButterHPF(f_cutoff, fs, order = order)
        elif approx == 'Chebyshev-1':
            b, a = designChebyshevHPF(f_cutoff, fs, rp = 0.5, order = order)
        elif approx == 'Chebyshev-2':
            b, a = designChebyshev2HPF(f_cutoff, fs, rs = 40, order = order)
        elif approx == 'Elliptic':
            b, a = designEllipticHPF(f_cutoff, fs, rp = 0.5, rs = 40, order = order)
        else:
            b, a = designBesselHPF(f_cutoff, fs, order = order)

        y_filtered = lfilter(b, a, data)
        return y_filtered
    

    # Pass the data through the bandpass filter
    def filterBandpass(self, data, f_lcut, f_hcut, fs, approx, order = 5):
        if approx == 'Butterworth':
            b, a = designButterBPF(f_lcut, f_hcut, fs, order = order)
        elif approx == 'Chebyshev-1':
            b, a = designChebyshevBPF(f_lcut, f_hcut, fs, rp = 0.5, order = order)
        elif approx == 'Chebyshev-2':
            b, a = designChebyshev2BPF(f_lcut, f_hcut, fs, rs = 40, order = order)
        elif approx == 'Elliptic':
            b, a = designEllipticBPF(f_lcut, f_hcut, fs, rp = 0.5, rs = 40, order = order)
        elif approx == 'Bessel':
            b, a = designBesselBPF(f_lcut, f_hcut, fs, order = order)
        else:
            b, a = designIIRPeak(f_hcut, fs, Q = 30)

        y_filtered = lfilter(b, a, data)
        return y_filtered


    def update(self):
        # Amplitude factor (default = 1)
        attenuation = tuple([1] * self.CHUNK)

        # Get time-domain data (audio stream)
        td_data = self.stream.read(self.CHUNK, exception_on_overflow = False)
        data_int = struct.unpack(str(self.CHUNK) + 'h', td_data)
    
        # Tuple multiplication for obtanining attenuated data_int stream.
        data_int = tuple(e1 * e2 for e1, e2 in zip(attenuation, data_int))

        self.setPlotData(name = 'waveform',
                         data_x = self.x,
                         data_y = data_int)

        # Filtering the raw audio data: bandpass, highpass or no filter
        currentFilterType = self.box_FilterType.currentText()
        currentFilterApprox = self.box_Approx.currentText()
        currentWindow = self.box_Window.currentText()


        # Windowing update
        if self.chkBox_windowEn.isChecked() and currentWindow == "Hann":
            window = hanningWindow(M = self.CHUNK)
            data_int *= window

        elif self.chkBox_windowEn.isChecked() and currentWindow == "Hamming":
            window = hammingWindow(M = self.CHUNK)
            data_int *= window

        elif self.chkBox_windowEn.isChecked() and currentWindow == "Rectangular":
            window = rectWindow(M = self.CHUNK)
            data_int *= window

        elif self.chkBox_windowEn.isChecked() and currentWindow == "Kaiser":
            window = kaiserWindow(M = self.CHUNK, beta = 14)
            data_int *= window

        elif self.chkBox_windowEn.isChecked() and currentWindow == "Blackman":
            window = blackmanWindow(M = self.CHUNK)
            data_int *= window

        elif self.chkBox_windowEn.isChecked() and currentWindow == "Flattop":
            window = flattopWindow(M = self.CHUNK)
            data_int *= window

        else: 
            data_int *= 1

        
        # Filtering update
        if self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())

            y_filtered = self.filterHighpass(data_int, f_low_cutoff, self.RATE, currentFilterApprox, filter_order)
            y_fft = fft(y_filtered)

        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            y_filtered = self.filterBandpass(data_int, f_low_cutoff, f_high_cutoff, self.RATE, currentFilterApprox, filter_order)
            y_fft = fft(y_filtered)

        else:
            y_fft = fft(data_int)


        sp_data = np.abs(y_fft[0:int(self.CHUNK / 2)]) / (128 * self.CHUNK)
        self.setPlotData(name = 'spectrum',
                         data_x = self.f,
                         data_y = sp_data)

        self.maxValFreq = self.f[np.argmax(sp_data[1::])]

        # Show the frequency at which the audio signal has the greatest
        # value. Later on, this will probably be used to decide if the motor
        # is running or not depending on the frequency at which it generates
        # a single tone.
        if (20 < self.maxValFreq < 20000) and (self.arg_verbose):
            print(f"Frequency: {int(self.maxValFreq)} Hz.")
            freqVal = self.maxValFreq
            self.statusText = "<b>Frequency:</b> {num:.2f} Hz."
            self.txt_Freq_Status.append(self.statusText.format(num = freqVal))
        
    
    def showWindowCurrentText(self):
        currentWindow = self.box_Window.currentText()
        self.txt_Status.append(f'<b>Window Function :</b> {currentWindow} is selected.')


    def showBoxFilterTypeCurrentText(self):
        currentFilterType = self.box_FilterType.currentText()
        self.txt_Status.append(f'<b>Filter Type :</b> {currentFilterType} is selected.')

        if (currentFilterType == 'Bandpass'):
            self.lbl_Cutoff_2.setVisible(True)
            self.txt_Cutoff_2.setVisible(True)
            self.lbl_Cutoff_1.setText('        Lower Cutoff (Hz)')
            self.box_Approx.addItem('IIR Peak')

        if (currentFilterType == 'Highpass'):
            self.lbl_Cutoff_2.setVisible(False)
            self.txt_Cutoff_2.setVisible(False)
            self.lbl_Cutoff_1.setText('          Cutoff Freq. (Hz)')
            self.box_Approx.removeItem(self.box_Approx.findText('IIR Peak'))


    def snapshot(self):
        date = datetime.now()
        fileName_TD = date.strftime('%Y-%m-%d_%H-%M-%S_TD.png')
        fileName_FD = date.strftime('%Y-%m-%d_%H-%M-%S_FD.png')
        p_TD = self.graphWidget_TimeDomain.grab()
        p_FD = self.graphWidget_FreqDomain.grab()
        p_TD.save(fileName_TD, 'png')
        p_FD.save(fileName_FD, 'png')
        self.txt_Status.append(f"Time-domain plot is saved.")
        self.txt_Status.append(f"Frequency-domain plot is saved.")


    def showBoxFilterOrderCurrentText(self):
        self.txt_Status.append(f"<b>Filter Order :</b> {self.box_FilterOrder.currentText()} is selected.")
    

    def showApproxCurrentText(self):
        self.txt_Status.append(f"<b>Approximation :</b> {self.box_Approx.currentText()} is selected.")
    

    def updateFilterStatus(self):
        if self.chkBox_filterEn.isChecked():
            self.txt_Status.append('<b>Filter enabled...</b>')
            self.lbl_FilterType.setEnabled(True)
            self.lbl_Approx.setEnabled(True)
            self.lbl_FilterOrder.setEnabled(True)
            self.lbl_Cutoff_1.setEnabled(True)
            self.lbl_Cutoff_2.setEnabled(True)
            self.box_FilterType.setEnabled(True)
            self.box_Approx.setEnabled(True)
            self.box_FilterOrder.setEnabled(True)
            self.txt_Cutoff_1.setEnabled(True)
            self.txt_Cutoff_2.setEnabled(True)
            self.btn_FilterResponse.setEnabled(True)

        else:
            self.txt_Status.append('<b>Filter disabled...</b>')
            self.lbl_FilterType.setEnabled(False)
            self.lbl_Approx.setEnabled(False)
            self.lbl_FilterOrder.setEnabled(False)
            self.lbl_Cutoff_1.setEnabled(False)
            self.lbl_Cutoff_2.setEnabled(False)
            self.box_FilterType.setEnabled(False)
            self.box_Approx.setEnabled(False)
            self.box_FilterOrder.setEnabled(False)
            self.txt_Cutoff_1.setEnabled(False)
            self.txt_Cutoff_2.setEnabled(False)
            self.btn_FilterResponse.setEnabled(False)
    

    def updateWindowStatus(self):
        if self.chkBox_windowEn.isChecked():
            self.txt_Status.append('<b>Windowing enabled...</b>')
            self.lbl_Window.setEnabled(True)
            self.box_Window.setEnabled(True)
            self.btn_WindowResponse.setEnabled(True)
        
        else:
            self.txt_Status.append('<b>Windowing disabled...</b>')
            self.lbl_Window.setEnabled(False)
            self.box_Window.setEnabled(False)
            self.btn_WindowResponse.setEnabled(False)
    

    def plotFilterResponse(self):
        plotFont = {'family' : 'Arial',
                    'weight' : 'bold',
                    'size'   : 13}

        mpl.rc('font', **plotFont)
        mpl.rcParams['toolbar'] = 'None'
        mpl.rcParams['axes.linewidth'] = 2.5

        filter_worN = 2**12

        plt.figure(1)
        plt.clf()

        currentFilterType = self.box_FilterType.currentText()
        currentFilterApprox = self.box_Approx.currentText()

        if self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass' and currentFilterApprox == 'Butterworth':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())
            
            # Design the filter
            b, a = designButterHPF(f_cutoff = f_low_cutoff, fs = self.RATE, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)

            plt.title('Butterworth High Pass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight='bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass' and currentFilterApprox == 'Chebyshev-1':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designChebyshevHPF(f_cutoff = f_low_cutoff, fs = self.RATE, rp = 0.5, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Chebyshev-1 Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 8000, 
                     y = 0.04,
                     s = "Passband ripple: 0.5 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass' and currentFilterApprox == 'Chebyshev-2':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designChebyshev2HPF(f_cutoff = f_low_cutoff, fs = self.RATE, rs = 40, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Chebyshev-2 Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 8000, 
                     y = 0.04,
                     s = "Stopband attenuation: 40 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass' and currentFilterApprox == 'Elliptic':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designEllipticHPF(f_cutoff = f_low_cutoff, fs = self.RATE, rp = 0.5, rs = 40, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Elliptic High Pass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 9000, 
                     y = 0.16,
                     s = "Passband ripple: 0.5 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.text(x = 7000, 
                     y = 0.04,
                     s = "Stopband attenuation: 40 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Highpass' and currentFilterApprox == 'Bessel':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designBesselHPF(f_low_cutoff, fs = self.RATE, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Bessel High Pass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.show()

        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'Butterworth':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designButterBPF(f_lc = f_low_cutoff, f_hc = f_high_cutoff, fs = self.RATE, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)

            plt.title('Butterworth Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'Chebyshev-1':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designChebyshevBPF(f_hc = f_high_cutoff, f_lc = f_low_cutoff, fs = self.RATE, rp = 0.5, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Chebyshev-1 Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 8000, 
                     y = 0.04,
                     s = "Passband ripple: 0.5 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'Chebyshev-2':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designChebyshev2BPF(f_hc = f_high_cutoff, f_lc = f_low_cutoff, fs = self.RATE, rs = 40, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Chebyshev-2 Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 8000, 
                     y = 0.04,
                     s = "Stopband attenuation: 40 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'Elliptic':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designEllipticBPF(f_hc = f_high_cutoff, f_lc = f_low_cutoff, fs = self.RATE, rp = 0.5, rs = 40, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Elliptic Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.text(x = 9000, 
                     y = 0.16,
                     s = "Passband ripple: 0.5 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.text(x = 7000, 
                     y = 0.04,
                     s = "Stopband attenuation: 40 dB", 
                     bbox = {'facecolor': 'none', 'alpha': 0.2, 'pad': 4},
                     fontsize = 9, 
                     horizontalalignment = 'center',
                     verticalalignment = 'center')
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'Bessel':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designBesselBPF(f_low_cutoff, f_high_cutoff, fs = self.RATE, order = filter_order)
            # Get the frequency response of the filter
            w, h = freqz(b, a, worN = filter_worN)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot((self.RATE * 0.5 / np.pi) * w, abs(h), 
                      label = "Order = %d" % filter_order, 
                      linewidth = 3, 
                      color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('Bessel Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.show()
        
        elif self.chkBox_filterEn.isChecked() and currentFilterType == 'Bandpass' and currentFilterApprox == 'IIR Peak':
            f_low_cutoff = float(self.txt_Cutoff_1.text())
            f_high_cutoff = float(self.txt_Cutoff_2.text())
            filter_order = float(self.box_FilterOrder.currentText())

            # Design the filter
            b, a = designIIRPeak(f0 = f_high_cutoff, fs = self.RATE, Q = 30)
            # Get the frequency response of the filter
            freq, h = freqz(b, a, fs = self.RATE)

            # Plot the response and -3 dB point
            plt.xscale("log")
            plt.plot(freq, 
                     20*np.log10(np.maximum(abs(h), 1e-5)), 
                     label = "Order = %d" % filter_order, 
                     linewidth = 3, 
                     color = 'black')
            plt.plot([0, 0.5 * self.RATE], 
                     [np.sqrt(0.5), np.sqrt(0.5)],
                     '--', 
                     label = 'Half Power', 
                     linewidth = 3)
            
            plt.title('2nd Order IIR Peak Bandpass Filter Magnitude Response', fontweight = 'bold')
            plt.xlabel('Frequency (Hz)', fontweight = 'bold')
            plt.ylabel('Gain', fontweight = 'bold')
            plt.grid(True)
            plt.legend(loc = 'best', framealpha = 1, fancybox = False)
            plt.tight_layout()
            plt.show()

        else:
            print("What?")
    

    def plotWindowResponse(self):
        plotFont = {'family' : 'Arial',
                    'weight' : 'bold',
                    'size'   : 12}

        mpl.rc('font', **plotFont)
        mpl.rcParams['toolbar'] = 'None'
        mpl.rcParams['axes.linewidth'] = 2.5
        mpl.rcParams['figure.figsize'] = (6, 8)

        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        currentWindowType = self.box_Window.currentText()

        if self.chkBox_windowEn.isChecked() and currentWindowType == "Hann":
            currWindow = hanningWindow(M = self.CHUNK)
            ax1.set_title("Hann Window", fontweight = 'bold')
            ax2.set_title("Hann Window Frequency Response", fontweight = 'bold')

        elif self.chkBox_windowEn.isChecked() and currentWindowType == "Hamming":
            currWindow = hammingWindow(M = self.CHUNK)
            ax1.set_title("Hamming Window", fontweight = 'bold')
            ax2.set_title("Hamming Window Frequency Response", fontweight = 'bold')
        
        elif self.chkBox_windowEn.isChecked() and currentWindowType == "Rectangular":
            currWindow = rectWindow(M = self.CHUNK)
            ax1.set_title("Rectangular (Boxcar) Window", fontweight = 'bold')
            ax2.set_title("Rectangular (Boxcar) Window Frequency Response", fontweight = 'bold')
        
        elif self.chkBox_windowEn.isChecked() and currentWindowType == "Kaiser":
            currWindow = kaiserWindow(M = self.CHUNK, beta = 14)
            ax1.set_title("Kaiser Window", fontweight = 'bold')
            ax2.set_title("Kaiser Window Frequency Response", fontweight = 'bold')
        
        elif self.chkBox_windowEn.isChecked() and currentWindowType == "Blackman":
            currWindow = blackmanWindow(M = self.CHUNK)
            ax1.set_title("Blackman Window", fontweight = 'bold')
            ax2.set_title("Blackman Window Frequency Response", fontweight = 'bold')
        
        elif self.chkBox_windowEn.isChecked() and currentWindowType == "Flattop":
            currWindow = flattopWindow(M = self.CHUNK)
            ax1.set_title("Flattop Window", fontweight = 'bold')
            ax2.set_title("Flattop Window Frequency Response", fontweight = 'bold')

        else:
            print("What?")

        ax1.plot(currWindow, linewidth = 3, color = 'black')
        ax1.set_xlabel("Sample", fontweight = 'bold')
        ax1.set_ylabel("Amplitude", fontweight = 'bold')

        freq_resp = fft(currWindow, self.CHUNK) / (len(currWindow)/2.0)
        f = np.linspace(-0.5, 0.5, len(freq_resp))
        freq_resp = np.abs(fftshift(freq_resp / abs(freq_resp).max()))
        freq_resp = 20 * np.log10(np.maximum(freq_resp, 1e-10))

        ax2.plot(f, freq_resp, linewidth = 3, color = 'black')
        ax2.set_xlabel("Normalized Frequency [cyc/sample]", fontweight = 'bold')
        ax2.set_ylabel("Normalized Magnitude [dB]", fontweight = 'bold')
        ax2.set_xlim([-0.5, 0.5])
        ax2.set_xticks(np.linspace(-0.5, 0.5, 11))

        plt.show()
        plt.tight_layout()


    # Exit the program.
    def exitProgram(self, event):
        quitMessage = "Are you sure you want to exit the program?"

        reply = QtGui.QMessageBox.question(self, 'Exit Program?', quitMessage, QtGui.QMessageBox.Yes, 
                                                                               QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if not self.arg_nologs:
                saveLog(self.txt_Status)
                
            print("Program exited successfully...")
            sys.exit()
    

    # Clear status texts.
    def clearStatusPane(self):
        self.txt_Status.clear()
        self.txt_Freq_Status.clear()


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()
    

    def showAbout(self):
        aboutMsgStyle = QApplication.style()
        aboutMsg = QMessageBox()
        aboutMsg.setWindowTitle("About Me")
        aboutMsg.setIcon(QMessageBox.Information)
        aboutMsg.setText('<b>Real-Time Audio Analyzer</b>')
        aboutMsg.setInformativeText("Version: 3.3" + "<br>Date: 2021-03-16" + 
                                                    "<br>Cihan Asci, 2021, Nanolab, Tufts" + 
                                                    "<br>Report an Issue: cihan.asci@tufts.edu" +
                                                    "<br>OS: Windows 10 Pro 64-bit")
        aboutMsg.setWindowIcon(QtGui.QIcon(aboutMsgStyle.standardIcon(QStyle.SP_DialogApplyButton)))
        aboutMsg.exec_()
    
    
    def openWindow2(self):
        self.helpWindow = HelpWindow()
        self.helpWindow.show()

    
    def exitMenuButtonOnClick(self):
        quitMessage = "Are you sure you want to exit the program?"

        reply = QtGui.QMessageBox.question(self, 'Exit Program?', quitMessage, QtGui.QMessageBox.Yes, 
                                                                               QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if not self.arg_nologs:
                saveLog(self.txt_Status)
            
            print("Program exited successfully...")
            qApp.quit()


    def closeEvent(self, event):
        quitMessage = "Are you sure you want to exit the program?"

        reply = QtGui.QMessageBox.question(self, 'Exit Program?', quitMessage, QtGui.QMessageBox.Yes, 
                                                                               QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                self.helpWindow.close()
            except AttributeError:
                print("Ignoring AttributeError...")

            if not self.arg_nologs:
                saveLog(self.txt_Status)
            
            print("Program exited successfully...")

            event.accept()
        else:
            event.ignore()
