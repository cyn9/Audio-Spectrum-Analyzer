#!/usr/bin/python
import platform

print("""Python version: %s
Python branch: %s
Python build version: %s
Python compiler version: %s
Python implementation: %s
""" % (
platform.python_version(),
platform.python_branch(),
platform.python_build(),
platform.python_compiler(),
platform.python_implementation(),
))
