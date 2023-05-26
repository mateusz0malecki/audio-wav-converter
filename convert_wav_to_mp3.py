from pydub import AudioSegment
from os import listdir
from os.path import isfile, join

only_files = [f for f in listdir("wav_files") if isfile(join("wav_files", f))]

for f in only_files:
    audio = AudioSegment.from_file(f"wav_files/{f}")
    new_filename = f"CONVERTED - {f.split('.')[0]}.mp3"
    audio.export(new_filename, format="mp3", bitrate="128k")
