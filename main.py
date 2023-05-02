from audio import tests as audio_tests
from video import tests as video_tests
from mp import tests as mediapipe_tests


def audio_tests_to_run() -> None:
	# audio_tests.grab_devices_test()
	# audio_tests.play_audio_test()
	# audio_tests.play_audio_to_device_test(device="Headphones (Realtek(R) Audio)")
	# audio_tests.passthrough_audio_test()
	pass


def video_tests_to_run() -> None:
	# video_tests.grab_webcam_ids_tests()
	# video_tests.grab_webcam_dimensions_test(cam_id=0)
	# video_tests.draw_landmarks_test()
	# video_tests.video_passthrough_test()
	pass


def mediapipe_tests_to_run() -> None:
	# mediapipe_tests._grab_frame(multi_handed=False)
	# mediapipe_tests.test_detection_results(multi_handed=True)
	pass


if (__name__ == "__main__"):
	audio_tests_to_run()
	video_tests_to_run()
	mediapipe_tests_to_run()
