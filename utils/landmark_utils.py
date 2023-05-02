import cv2
import numpy as np

from itertools import product
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from mediapipe.python.solutions.holistic import Holistic, HAND_CONNECTIONS


def detect_landmarks(image: np.ndarray, model: Holistic) -> dict[str, NormalizedLandmarkList]:
	"""
	Scans the provided image/video-frame and checks for the presense of a Hand(s). Returns a 
    dictionary with the Hand as key, and resulting `Mediapipe NormalizedLandmarkList` as the value.

	Parameters
	----------
	image: np.ndarray
		`Numpy nD-Array` of type `Float64`
	model: `Mediapipe Holistic` Model

	Returns
	-------
	`Numpy nD-Array` of type `Float64` and shape `(21,3)`
	"""
	image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
	image.setflags(write=False)

	result = model.process(image=image)

	return {
		"left": result.left_hand_landmarks,
		"right": result.right_hand_landmarks,
	}


def extract_all_angles(detections: dict[str, NormalizedLandmarkList]) -> dict[str, np.ndarray[np.float64]]:
	result = {}

	for hand, landmarks in detections.items():
		if (not landmarks):
			result[hand] = np.zeros(shape=441)
			continue

		processed = np.nan_to_num(x=[
			[landmark.x, landmark.y, landmark.z] 
            for landmark in landmarks.landmark
	    ])

		connections = map(lambda t: processed[t[1]] - [t[0]], HAND_CONNECTIONS)

		angles_list = []
		for connection in product(connections, repeat=2):
			angle = _get_angle_between_connections(u=connection[0], v=connection[1])

			angles_list.append(angle if (angle == angle) else 0)

		result[hand] = np.array(angles_list)

	return result


def _get_angle_between_connections(u: np.ndarray, v: np.ndarray) -> np.float64:
	"""
	Calculates the Angle between a pair of Connections (A Connection is the direct Vector 
    between two Keypoints) and returns it as a `Numpy Float64`

	Parameters
	----------
	u, v: `Numpy nD-Array`
		A 3D Vector representing a Connection

	Returns
	----------
	`Numpy Float64`
	"""
	if (np.array_equal(u, v)):
		return np.float64(0)

	dot_product = np.dot(a=u, b=v)
	norm = np.linalg.norm(x=u) * np.linalg.norm(x=v)

	return np.arccos(dot_product / norm)
