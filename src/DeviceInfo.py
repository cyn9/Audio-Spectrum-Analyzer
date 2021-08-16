'''
Function implemented from the source: https://github.com/jleb/pyaudio
'''

from pyqtgraph.Qt import QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle

import pyaudio

# Standard audio sample rates:
std_sample_rates = [8000.0, 9600.0, 11025.0, 12000.0,
                    16000.0, 22050.0, 24000.0, 32000.0,
                    44100.0, 48000.0, 88200.0, 96000.0,
                    192000.0]


# statusText: Reference to status textfield
# pIns: Reference instance to pyaudio object (p)
def getDeviceInfo(statusText, pInst):
    maxAPIs = pInst.get_host_api_count()
    maxDevs = pInst.get_device_count()

    # PortAudio info:
    statusText.append(f"Audio System Info:")
    statusText.append(f"Version: {pyaudio.get_portaudio_version()}.")
    statusText.append(f"Number of Host APIs: {maxAPIs}.")
    statusText.append(f"Number of Devices  : {maxDevs}.")
    
    # Host API info:
    statusText.append(f"Host API Info:")
    
    for i in range(maxAPIs):
        API_Info = pInst.get_host_api_info_by_index(i)

        for k in list(API_Info.items()):
            statusText.append(f"{k}: {k}")
        
        statusText.append("--------------------------")
    
    # Device List:
    for i in range(maxDevs):
        inputSupportedRates  = []
        outputSupportedRates = []
        fullDuplexRates      = []

        devInfo = pInst.get_device_info_by_index(i)

        for k in list(devInfo.items()):
            name, value = k

            if name == 'hostApi':
                value = str(value) + \
                    " (%s)" % pInst.get_host_api_info_by_index(k[1])['name']
            
            statusText.append(f"   {name}: {value}")

        for rate in std_sample_rates:
            if devInfo['maxInputChannels'] > 0:
                try:
                    if pInst.is_format_supported(
                        rate,
                        input_device    = devInfo['index'],
                        input_channels  = devInfo['maxInputChannels'],
                        input_format    = pyaudio.paInt16):
                        inputSupportedRates.append(rate)
                except ValueError:
                    pass
            
            if devInfo['maxOutputChannels'] > 0:
                try:
                    if pInst.is_format_supported(
                        rate,
                        output_device   = devInfo['index'],
                        output_channels = devInfo['maxOutputChannels'],
                        output_format   = pyaudio.paInt16):
                        outputSupportedRates.append(rate)
                except ValueError:
                    pass
            
            if (devInfo['maxInputChannels'] > 0) and (devInfo['maxOutputChannels'] > 0):
                try:
                    if pInst.is_format_supported(
                        rate,
                        input_device    = devInfo['index'],
                        input_channels  = devInfo['maxInputChannels'],
                        input_format    = pyaudio.paInt16,
                        output_device   = devInfo['index'],
                        output_channels = devInfo['maxOutputChannels'],
                        output_format   = pyaudio.paInt16):
                        fullDuplexRates.append(rate)
                except ValueError:
                    pass
            
        if len(inputSupportedRates):
            statusText.append("  Input rates: {inputSupportedRates}")

        if len(outputSupportedRates):
            statusText.append("  Output rates: {outputSupportedRates}")

        if len(fullDuplexRates):
            statusText.append("  Full duplex rates: {fullDuplexRates}")

    
    # Default device info:
    statusText.append("\nDefault Devices:\n")

    try:
        defaultIndex = pInst.get_default_input_device_info()['index']
        statusText.append(f"Default device index = {defaultIndex}")

        deviceIndex = pInst.get_device_info_by_index(defaultIndex)
        for k in list(deviceIndex.items()):
            name, value = k

            if name == 'hostApi':
                value = str(value) + \
                        " (%s)" % pInst.get_host_api_info_by_index(k[1])['name']
                
                statusText.append("   {name}: {value}")

        statusText.append("--------------------------")

    except IOError as e:
        errorFlag = e[0]
        statusText.append("No input devices found: {errorFlag}.")

        errorMsg = QMessageBox()
        errorMsg.setWindowTitle("Input Device Warning")
        errorMsg.setIcon(QMessageBox.Information)
        errorMsg.setText('Input Device Warning')
        errorMsg.setInformativeText("No input devices found...")

        errorMsg.setWindowIcon(QtGui.QIcon(errorMsg.standardIcon(QStyle.SP_DialogApplyButton)))
        errorMsg.exec_()
    
    try:
        defaultIndex = pInst.get_default_output_device_info()['index']
        statusText.append(f"Default Output Device: {defaultIndex}")

        devinfo = pInst.get_device_info_by_index(defaultIndex)

        for k in list(devinfo.items()):
            name, value = k
            if name == 'hostApi':
                value = str(value) + \
                        " (%s)" % pInst.get_host_api_info_by_index(k[1])['name']
            statusText.append("  %s: %s" % (name, value))
        statusText.append("--------------------------------")
    
    except IOError as e:
        errorFlag = e[0]
        statusText.append(f"No input devices found: {errorFlag}.")

        errorMsg = QMessageBox()
        errorMsg.setWindowTitle("Input Device Warning")
        errorMsg.setIcon(QMessageBox.Information)
        errorMsg.setText('Input Device Warning')
        errorMsg.setInformativeText("No input devices found...")

        errorMsg.setWindowIcon(QtGui.QIcon(errorMsg.standardIcon(QStyle.SP_DialogApplyButton)))
        errorMsg.exec_()
