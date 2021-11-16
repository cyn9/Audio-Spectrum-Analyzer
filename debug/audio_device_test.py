'''
Functionality implemented from the source: https://github.com/jleb/pyaudio
'''

import pyaudio
import platform

# Standard audio sample rates:
std_sample_rates = [8000.0, 9600.0, 11025.0, 12000.0,
                    16000.0, 22050.0, 24000.0, 32000.0,
                    44100.0, 48000.0, 88200.0, 96000.0,
                    192000.0]

inputDevices = list()

# PyAudio object initialization
FORMAT   = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024 * 2

p = pyaudio.PyAudio()

if platform.system() == "Darwin":
    RATE = 48000
else:
    RATE = 44100

chosen_device_index = -1
for x in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(x)

    if info["name"] == "pulse":
        chosen_device_index = info["index"]
        print(f"Chosen index: {chosen_device_index}")
            
try:
    stream = p.open(
        format             = FORMAT,
        channels           = CHANNELS,
        rate               = RATE,
        input_device_index = chosen_device_index,
        input              = True,
        output             = False,
        frames_per_buffer  = CHUNK
    )
except OSError:
    print("No audio input device is found.")


maxAPIs = p.get_host_api_count()
maxDevs = p.get_device_count()

# PortAudio info:
print(f"Audio System Info:")
print(f"Version : {pyaudio.get_portaudio_version()}.")
print(f"Number of Host APIs : {maxAPIs}.")
print(f"Number of Devices   : {maxDevs}.")

print(f"\nHost API Info:")

for i in range(maxAPIs):
    API_Info = p.get_host_api_info_by_index(i)

    for k in list(API_Info.items()):
        print(f"{k}: {k}")
    
    print("--------------------------")

# Device List:
for i in range(maxDevs):
    inputSupportedRates  = []
    outputSupportedRates = []
    fullDuplexRates      = []

    devInfo = p.get_device_info_by_index(i)

    for k in list(devInfo.items()):
        name, value = k

        if name == 'hostApi':
            value = str(value) + \
                " (%s)" % p.get_host_api_info_by_index(k[1])['name']
        
        print(f"   {name}: {value}")

    for rate in std_sample_rates:
        if devInfo['maxInputChannels'] > 0:
            try:
                if p.is_format_supported(
                    rate,
                    input_device    = devInfo['index'],
                    input_channels  = devInfo['maxInputChannels'],
                    input_format    = pyaudio.paInt16):
                    inputSupportedRates.append(rate)
            except ValueError:
                pass
        
        if devInfo['maxOutputChannels'] > 0:
            try:
                if p.is_format_supported(
                    rate,
                    output_device   = devInfo['index'],
                    output_channels = devInfo['maxOutputChannels'],
                    output_format   = pyaudio.paInt16):
                    outputSupportedRates.append(rate)
            except ValueError:
                pass
        
        if (devInfo['maxInputChannels'] > 0) and (devInfo['maxOutputChannels'] > 0):
            try:
                if p.is_format_supported(
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
        print("  Input rates: {inputSupportedRates}")

    if len(outputSupportedRates):
        print("  Output rates: {outputSupportedRates}")

    if len(fullDuplexRates):
        print("  Full duplex rates: {fullDuplexRates}")

print("\nDefault Devices:\n")

try:
    defaultIndex = p.get_default_input_device_info()['index']
    print(f"Default device index = {defaultIndex}")

    deviceIndex = p.get_device_info_by_index(defaultIndex)
    for k in list(deviceIndex.items()):
        name, value = k

        if name == 'hostApi':
            value = str(value) + \
                    " (%s)" % p.get_host_api_info_by_index(k[1])['name']
            
            print("   {name}: {value}")

    print("--------------------------")

except IOError as e:
    errorFlag = e[0]
    print("No input devices found: {errorFlag}.")

    print('Input Device Warning')
    print("No input devices found...")


try:
    defaultIndex = p.get_default_output_device_info()['index']
    print(f"Default Output Device: {defaultIndex}")

    devinfo = p.get_device_info_by_index(defaultIndex)

    for k in list(devinfo.items()):
        name, value = k
        if name == 'hostApi':
            value = str(value) + \
                    " (%s)" % p.get_host_api_info_by_index(k[1])['name']
        print("  %s: %s" % (name, value))
    print("--------------------------------")

except IOError as e:
    errorFlag = e[0]
    print(f"No input devices found: {errorFlag}.")

    print('Input Device Warning')
    print("No input devices found...")
