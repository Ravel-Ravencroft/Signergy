from pathlib import Path

from video import functionality


ROOT_DIR = Path(__file__).parents[1].resolve()
TEST_FILE = str(ROOT_DIR / "test_files/test_video.mp4")


def grab_webcam_ids_tests() -> None:
	print("\nAvailable WebCam Devices:")
	device_list = functionality.get_camera_ids()

	if (not device_list):
		print("\tNo WebCam Devices Available on the Host System!")
		return

	{print(f"\t{device}") for device in device_list}


def grab_webcam_dimensions_test(cam_id) -> None:
	print("\nWebCam Dimensions:")
	{print(f"\t{key}: {value}") for key, value in functionality.get_camera_dimensions(camera_id=cam_id).items()}


def draw_landmarks_test() -> None:
	functionality.draw_landmarks()


def video_passthrough_test() -> None:
	functionality.video_passthrough(input_stream=TEST_FILE)

