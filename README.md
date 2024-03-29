# OBS Studio Recording Demultiplexer

A script for OBS Studio to separate out tracks in recordings automatically.


## OBS Scripting Setup

To setup [OBS Studio](https://obsproject.com/) for Python scripts, you must have Python 3.6 or higher installed. OBS Studio supports current Python versions now on Windows, so grab the latest stable "Windows installer (64-bit)" build available at [python.org](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe). After ensuring Python 3.6+ is installed, open OBS Studio, select "Tools" from the menu bar and "Scripts" from the menu, go to the "Python Settings" tab, and select the base prefix for Python 3.6+. For Windows, the base prefix will be `%LOCALAPPDATA%\Programs\Python\Python310` (for Python 3.10). To load scripts, go back to the "Scripts" tab and click the "+" in the lower-left and navigate to the appropriate script file.


## Recording Demux Setup

The recording demultiplexer has a requirement that FFmpeg is available either adjacent to the script file or in the system PATH. Static builds of FFmpeg are available from https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip and to use these builds, place the `ffmpeg` and `ffprobe` files from the `bin` folder into the same folder as the script. Additionally, the ffmpeg-python package from PyPI must be installed in the Python path. To install this in Windows, open a PowerShell or CMD command prompt and run the command `%LOCALAPPDATA%\Programs\Python\Python310\Scripts\pip.exe install -U ffmpeg-python` (for Python 3.10).


## Usage

The path for FFmpeg is automatically determined and the script is enabled by default after being added to demux all recordings from OBS in the same directory as recordings are made following a name format of `<recording>.<tracknum>.mkv` for video tracks and `<recording>.<tracknum>.mka` for audio tracks. There is a checkbox in the script settings to disable the functionality of the script or to provide alternative paths for `ffmpeg` and `ffprobe`.
