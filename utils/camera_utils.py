import cv2
import numpy as np

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS
from mediapipe.python.solutions import drawing_styles, drawing_utils

from utils import io_utils


def update_frame(image: np.ndarray) -> np.ndarray:
	dims = io_utils.get_screen_dimensions()

	image = cv2.resize(
		src=image, dsize=(dims["width"], dims["height"]), interpolation=cv2.INTER_AREA
	)

	return image


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
