#!/usr/bin/python
import platform

print("""Operation System (OS): %s
OS Kernel Version: %s
OS Release Version: %s
OS Platform: %s
MAC Version: %s
uname: %s
Architecture: %s
Machine: %s
""" % (
platform.system(),
platform.version(),
platform.release(),
platform.platform(),
platform.mac_ver(),
platform.uname(),
platform.architecture(),
platform.machine(),
))
