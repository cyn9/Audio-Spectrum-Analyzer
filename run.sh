#!/bin/sh

echo "Collecting system information..."

mkdir -p info

OUTPUT_FILE=info/env_log.txt

{
echo
echo '## Python Check ##'
} >> ${OUTPUT_FILE}

cat << EOF > info/python_test.py
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
EOF

python3 info/python_test.py 2>&1 >> ${OUTPUT_FILE}
echo 'Python test complete.'

{
echo
echo '## Platform Check ##'
} >> ${OUTPUT_FILE}

cat << EOF > info/platform_test.py
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
EOF

python3 info/platform_test.py 2>&1 >> ${OUTPUT_FILE}
echo 'Platform test complete.'
echo ''

python3 src/run.py "$@"