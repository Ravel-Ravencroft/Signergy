import cv2
import pyvirtualcam

from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
from mediapipe.python.solutions import drawing_utils as mp_drawing


def get_camera_ids() -> set[int]:
	index = 0
	camera_list = set()

	while True:
		cap = cv2.VideoCapture(index=index)
		has_frame = cap.read()[0]
		cap.release()

		if (not has_frame):
			break

		camera_list.add(index)
		index += 1

	return camera_list


def get_camera_dimensions(camera_id: int = 0) -> dict[str, int]:
	cap = cv2.VideoCapture(camera_id)
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(cap.get(cv2.CAP_PROP_FPS))
	cap.release()

	return {"width": width, "height": height, "fps": fps}


def draw_landmarks(input_device: int = 0) -> None:
	# For webcam input:
	cap = cv2.VideoCapture(input_device)

	with Hands(
		model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
	) as hands:
		while cap.isOpened():
			has_frame, image = cap.read()

			if not has_frame:
				continue

			# Marks the image as not writeable to pass by reference and thus improve performance.
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = hands.process(image)

			# Draw the hand annotations on the image.
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

			if (results.multi_hand_landmarks):
				for hand_landmarks in results.multi_hand_landmarks:
					mp_drawing.draw_landmarks(
						image,
						hand_landmarks,
						HAND_CONNECTIONS,
						mp_drawing_styles.get_default_hand_landmarks_style(),
						mp_drawing_styles.get_default_hand_connections_style(),
					)

			# Flip the image horizontally for a selfie-view display.
			cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))

			if cv2.waitKey(10) & 0xFF == ord("q"):
				break

		cv2.destroyAllWindows()

	cap.release()


def video_passthrough(input_stream: int | str = 0) -> None:
	cap = cv2.VideoCapture(input_stream)
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(cap.get(cv2.CAP_PROP_FPS))

	with (pyvirtualcam.Camera(width=width, height=height, fps=fps) as cam):
		print(f"Using Virtual Camera: {cam.device}")

		while cap.isOpened():
			# Read feed
			_, frame = cap.read()

			frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

			cam.send(frame)
			cam.sleep_until_next_frame()

	cap.release()
