from pathlib import Path

from audio import functionality


ROOT_DIR = Path(__file__).parents[1].resolve()
TEST_FILE = ROOT_DIR / "test_files/test_audio.mp3"


def grab_devices_test() -> None:
	print("\nAvailable Audio Input Devices:")
	{print(f"\t{device}") for device in functionality.get_audio_devices()}

	print("\nAvailable Audio Output Devices:")
	{print(f"\t{device}") for device in functionality.get_audio_devices(is_input=False)}


def play_audio_test() -> None:
	print("Playing Sample Audio on Default Output Device!")

	functionality.play_audio(audio_file=TEST_FILE)
	print("\tAudio Playback Complete!")


def play_audio_to_device_test(device: str) -> None:
	print("Playing Sample Audio on Specified Output Device!")

	functionality.play_audio(audio_file=TEST_FILE, output=device)
	print("\tAudio Playback Complete!")


def passthrough_audio_test() -> None:
	print("""
		Playing Sample Audio on Passthrough Device! Please use a Video Conferencing Software such as Google Meet
		and shift the Microphone device to 'CABLE Output (VB-Audio Virtual Cable)' to test the Audio Passthrough Functionality!
	""")

	functionality.play_audio(audio_file=TEST_FILE, output="CABLE Input (VB-Audio Virtual Cable)")
	print("\tAudio Playback Complete!")
