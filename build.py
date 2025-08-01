import os
import subprocess
import sys
import shutil
import venv
from src.constants import *

# Define paths and script name
script_name = MAINSCRIPTPATH
icon_path = os.path.join(DATAFILESPATH, 'pyDatalink_icon.ico')
output_directory = PROJECTPATH
requirements_file = 'requirements.txt'
spec_file = APPNAME + '.spec'
venv_dir = 'venv'

import os
import venv

venv_dir = "venv"

if not os.path.exists(os.path.join(venv_dir, "bin", "python")):
    print("Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)
else:
    print("Virtual environment already exists. Skipping creation.")

print('Activate virtual environment')

if sys.platform == 'win32' :
    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') 
    venv_exe_path =  os.path.join(venv_dir, 'Scripts')
else :
    activate_script = os.path.join(venv_dir, 'bin', 'activate')
    venv_exe_path =  os.path.join(venv_dir, 'bin')
print('Install required python packages')
subprocess.run([f'{venv_exe_path}/python', '-m', 'pip', 'install', '-r', requirements_file])

print('Create the executable')
pyinstaller_command = [
    f'{venv_exe_path}/pyinstaller',
    '--name=' + APPNAME,
    '--onefile',
    '--icon=' + icon_path,
    '--distpath=' + output_directory,
    '--clean',
    '--noconfirm',
    '--noconsole',
    '--add-data=' + DATAFILESPATH +':data',
    script_name
]
try :
    status = subprocess.run(pyinstaller_command)
finally :
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists(spec_file):
        os.remove(spec_file)

    if sys.platform == 'win32':
        deactivate_script = os.path.join(venv_dir, 'Scripts', 'deactivate.bat')
    else:
        deactivate_script = os.path.join(venv_dir, 'bin', 'deactivate')


    subprocess.run(deactivate_script, shell=True)


    shutil.rmtree(venv_dir)
    try :
        if status.returncode == 0 :
            print('Build completed successfully!')
        else :
            print('Error while building the project')
    except : 
        print('Error while building the project')