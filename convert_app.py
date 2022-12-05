import os
import sys
from pydub import AudioSegment
from easygui import msgbox, ccbox, fileopenbox, exceptionbox


class ExtensionException(Exception):
    def __init__(self):
        super().__init__(
            "Unsupported file extension."
        )


def convert_to_wav_and_save_file(filepath: str):
    """
    Func to convert given audio file to WAV extension and save it as new file.
    :param filepath: path to local audio file in .mp3, .mp4 or .m4a extension
    :return: path to converted WAV file
    """
    extension_list = ("mp4", "mp3", "m4a")
    filename = filepath.split("\\")[-1]
    dir_ = filepath.replace(filename, '')
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    for extension in extension_list:
        if filename.lower().endswith(extension):
            audio = AudioSegment.from_file(filepath, extension)
            new_audio = audio.set_frame_rate(frame_rate=16000)
            new_filename = f"{dir_}CONVERTED - {filename.split('.')[0]}.wav"
            new_audio.export(new_filename, format="wav")
            return new_filename
    raise ExtensionException


title = "digimonkeys.com converter"
msg = """
Welcome to WAV converter. 
Supported audio extensions: MP4, MP3, M4A. 
FFmpeg installed on your local machine is required.
"""
msgbox(msg=msg, title=title)

while 1:
    msg = "Choose audio file from your local storage to convert it to WAV."
    if ccbox(
            msg=msg,
            title=title,
            choices=["Ch[o]ose file", "C[a]ncel"],
            default_choice='Choose file',
            cancel_choice='Cancel'
    ):
        file_path = fileopenbox()
        try:
            convert_to_wav_and_save_file(filepath=file_path)
            msgbox(msg="Converted file saved in the source file directory.", title=title)
        except ExtensionException:
            msgbox(msg="Unsupported file extension.", title=title)
        except AttributeError:
            pass
        except Exception as e:
            exceptionbox(str(e), title=title)
        pass
    else:
        sys.exit(0)
