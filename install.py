import subprocess
import sys

subprocess.run((sys.executable, '-m', 'pip', 'install', 'limeinstall'))

try:
    subprocess.run((sys.executable, '-m', 'limeinstall', *sys.argv[1:]))
finally:
    subprocess.run((sys.executable, '-m', 'pip', 'uninstall', 'limeinstall' ,'-y'))
