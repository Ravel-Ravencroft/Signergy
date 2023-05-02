import time

from pathlib import Path
from pygame import mixer
from pygame._sdl2 import audio


def get_audio_devices(is_input: bool=True) -> list[str]:
	# Initialize the mixer, which allows the next command to work
	mixer.init()

	# Grabs audio devices
	device_list = audio.get_audio_device_names(iscapture=is_input)

 	# Quit the mixer as it's initialized on your main playback device
	mixer.quit()

	return device_list


def play_audio(audio_file: Path | str, output: str=None) -> None:
	mixer.init(devicename=output)
	mixer.music.load(filename=audio_file)
	mixer.music.play()

	while mixer.music.get_busy():
		time.sleep(1)
	else:
		mixer.music.unload()

	mixer.quit()
