import cv2
import numpy as np

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from mediapipe.python.solutions import drawing_styles, drawing_utils
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS


def draw_landmarks(
	image: np.ndarray, landmarks: dict[str, NormalizedLandmarkList]
) -> None:
	for landmark_list in landmarks.values():
		drawing_utils.draw_landmarks(
			image,
			landmark_list=landmark_list,
			connections=HAND_CONNECTIONS,
			landmark_drawing_spec=drawing_styles.get_default_hand_landmarks_style(),
			connection_drawing_spec=drawing_styles.get_default_hand_connections_style(),
		)


def add_text(image: np.ndarray, text: str) -> np.ndarray:
	window_height, window_width, _ = image.shape
	offset = int(window_height * 0.02)

	(text_width, text_height), _ = cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)

	text_x = int((window_width - text_width) / 2)
	text_y = int(window_height - text_height - offset)

	cv2.rectangle(img=image, pt1=(0, text_y - offset), pt2=(window_width, window_height), color=(245, 242, 176, 0.85), thickness=-1)

	cv2.putText(
		img=image,
		text=text,
		org=(text_x, (text_y + text_height)),
		fontFace=cv2.FONT_HERSHEY_COMPLEX,
		fontScale=1,
		color=(118, 62, 37),
		thickness=2,
	)

	return image
