import cv2
import numpy as np

from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from typing import NamedTuple


def detect_landmarks(image: np.ndarray) -> NamedTuple:
	image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
	image.flags.writeable = False
	return Hands(
		min_detection_confidence=0.5, 
		min_tracking_confidence=0.5
	).process(image)


def draw_landmarks(image: np.ndarray, results: NamedTuple) -> np.ndarray:
	image = mp_drawing.draw_landmarks(
		image=image,
		landmark_list=results.left_hand_landmarks,
		connections=HAND_CONNECTIONS,
		landmark_drawing_spec=mp_drawing.DrawingSpec(
			color=(232, 254, 255), thickness=1, circle_radius=4
		),
		connection_drawing_spec=mp_drawing.DrawingSpec(
			color=(255, 249, 161), thickness=2, circle_radius=2
		),
	)

	image = mp_drawing.draw_landmarks(
		image=image,
		landmark_list=results.right_hand_landmarks,
		connections=HAND_CONNECTIONS,
		landmark_drawing_spec=mp_drawing.DrawingSpec(
			color=(232, 254, 255), thickness=1, circle_radius=4
		),
		connection_drawing_spec=mp_drawing.DrawingSpec(
			color=(255, 249, 161), thickness=2, circle_radius=2
		),
	)

	return image
