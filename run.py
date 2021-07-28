import os
import subprocess 
for x in range(0,10):
    command = 'python TTC.py'
    os.system(command)
    #or
    #subprocess.call('cmd ' + command, shell=True)