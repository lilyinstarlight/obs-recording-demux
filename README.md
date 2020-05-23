# OBS Studio Recording Demultiplexer

A script for OBS studio to separate out tracks in recordings automatically.


## General Script Setup

To setup [OBS Studio](https://obsproject.com/) for Python scripts, you must have Python 3.6 or higher installed. OBS Studio only supports Python 3.6 on Windows currently and the latest Windows installer available for it is [Python 3.6.8](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe). After ensuring Python 3.6+ is installed, open OBS Studio, select "Tools" from the menu bar and "Scripts" from the menu, go to the "Python Settings" tab, and select the base prefix for Python 3.6+. For Windows, the base prefix will be `%LOCALAPPDATA%\Programs\Python\Python36`. To load scripts, go back to the "Scripts" tab and click the "+" in the lower-left and navigate to the appropriate script file.


## Recording Demux Setup

The recording demultiplexer has a requirement that FFmpeg is available either adjacent to the script file or in the system PATH. Static builds of FFmpeg are available from https://ffmpeg.zeranoe.com/builds/ and to use these builds, place the `ffmpeg` and `ffprobe` files from the `bin` folder into the same folder as the script. Additionally, the ffmpeg-python package from PyPI must be installed in the Python path. To install this in Windows, open a PowerShell or CMD command prompt and run the command `%LOCALAPPDATA%\Programs\Python\Python36\Scripts\pip.exe install ffmpeg-python`.


## Usage

The path for FFmpeg is automatically determined and the script is enabled by default after being added to demux all recordings from OBS in the same directory as recordings are made following a name format of `<recording>.<tracknum>.mkv` for video tracks and `<recording>.<tracknum>.mka` for audio tracks. There is a checkbox in the script settings to disable the functionality of the script or to provide alternative paths for `ffmpeg` and `ffprobe`.
