import obspython as obs

import os
import os.path
import sys

import ffmpeg


formats = {
    'video': 'mkv',
    'audio': 'mka',
}

codec_args = {
    'audio': {'c:a': 'copy'},
    'video': {'c:v': 'copy'},
}


settings = None

children = []


def script_description():
    return '<b>Recording Demultiplexer</b><hr/>Demultiplex all tracks in recording outputs when recordings are made. This can be useful if you are recording multiple audio streams that would be preferred in separate files.<br/><br/>Requires "Standard" recording output type. "Custom Output (FFmpeg)" will not work.<br/><br/>Made by Lily Foster &lt;fkmclane@gmail.com&gt;'


def script_load(settings_):
    global settings

    settings = settings_

    obs.timer_add(check_children, 1000)

    obs.obs_frontend_add_event_callback(stop_recording_action)


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_bool(props, 'enabled', 'Enabled')
    obs.obs_properties_add_text(props, 'cmd_ffmpeg', 'Command: ffmpeg', obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, 'cmd_ffprobe', 'Command: ffprobe', obs.OBS_TEXT_DEFAULT)

    return props


def script_defaults(settings):
    obs.obs_data_set_default_bool(settings, 'enabled', True)

    if sys.platform == 'win32':
        suffix = '.exe'
    else:
        suffix = ''

    ffmpeg_path = os.path.join(os.path.dirname(__file__), f'ffmpeg{suffix}')
    if os.path.isfile(ffmpeg_path) and os.access(ffmpeg_path, os.X_OK):
        obs.obs_data_set_default_string(settings, 'cmd_ffmpeg', ffmpeg_path)
    else:
        obs.obs_data_set_default_string(settings, 'cmd_ffmpeg', f'ffmpeg{suffix}')

    ffprobe_path = os.path.join(os.path.dirname(__file__), f'ffprobe{suffix}')
    if os.path.isfile(ffprobe_path) and os.access(ffprobe_path, os.X_OK):
        obs.obs_data_set_default_string(settings, 'cmd_ffprobe', ffprobe_path)
    else:
        obs.obs_data_set_default_string(settings, 'cmd_ffprobe', f'ffprobe{suffix}')


def check_children():
    for child in children.copy():
        if child.poll() is not None:
            children.remove(child)
            if child.returncode != 0:
                print(f'ERROR: Subprocess exited with code {child.returncode}: {child.args}')


def stop_recording_action(event):
    if event != obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        return

    output = obs.obs_frontend_get_recording_output()
    output_settings = obs.obs_output_get_settings(output)

    video_path = obs.obs_data_get_string(output_settings, 'path')

    obs.obs_data_release(output_settings)
    obs.obs_output_release(output)

    print(f'Demultiplexing recording at "{video_path}"')

    children.append(demux(video_path))


def demux(infile):
    input = ffmpeg.input(infile)
    outputs = []

    for idx, stream in enumerate(ffmpeg.probe(infile, cmd=obs.obs_data_get_string(settings, 'cmd_ffprobe'))['streams']):
        outputs.append(ffmpeg.output(input[str(idx)], f'{infile.rsplit(".", 1)[0]}.{idx}.{formats[stream["codec_type"]]}', **codec_args[stream['codec_type']]))

    return ffmpeg.run_async(ffmpeg.merge_outputs(*outputs), cmd=obs.obs_data_get_string(settings, 'cmd_ffmpeg'), quiet=True, overwrite_output=True)
