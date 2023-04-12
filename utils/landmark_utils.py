import cv2
import numpy as np

from itertools import product
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS


def detect_landmarks(image: np.ndarray, model: Hands) -> dict[str, NormalizedLandmarkList]:
	"""
	Scans the provided image/video-frame and checks for the presense of a Hand(s). Returns a dictionary with the Hand as key, and resulting `Mediapipe NormalizedLandmarkList` as the value.

	Parameters
	----------
	image: np.ndarray
		`Numpy nD-Array` of type `Float64`
	model: `Mediapipe Hands` Model

	Returns
	-------
	`Numpy nD-Array` of type `Float64` and shape `(21,3)`
	"""
	image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
	image = cv2.flip(src=image, flipCode=1)
	image.setflags(write=False)

	result = model.process(image=image)

	return {
		str(classification.label).lower(): _extract_landmarks(landmarks)
			for hand in result.multi_handedness
				for classification, landmarks in zip(hand.classification, result.multi_hand_landmarks)
	}


def _extract_landmarks(landmarks: NormalizedLandmarkList | None) -> np.ndarray[np.float64]:
	"""
	If a hand was detected, extracts the X, Y and Z coordinates from the resulting `Mediapipe NormalizedLandmarkList` and returns them as a `Numpy nD-Array` of type `Float64` and  shape `(21,3)` (21 Landmarks in a Hand, 3 Coordinates per Landmark).

	If a hand wasn't detected, returns a `Numpy nD-Array` of type `Float64` and shape `(21,3)` filled with zeros.

	Parameters
	----------
	landmarks: `Mediapipe NormalizedLandmarkList`

	Returns
	-------
	`Numpy nD-Array` of type `Float64` and shape `(21,3)`
	"""
	if (not landmarks):
		return np.zeros(shape=(21, 3))

	return np.nan_to_num(
		x=[[landmark.x, landmark.y, landmark.z] for landmark in landmarks.landmark]
	)


def get_all_angles(landmarks: np.ndarray[np.float64]) -> list[np.float64]:
	"""
	Calculates the Angles between all pairs of Connections (A Connection is the direct Vector between two Keypoints) in a Hand (21 Keypoints in a Hand, 3 Coordinates per Keypoint), and returns a list of type `Numpy Float64` and length 441 (21 ^ 2).

	Parameters
	----------
	landmarks: `np.ndarray[np.float64]`
		`Numpy nD-Array` of type `Float64` and shape `(21,3)` 

	Returns
	----------
	List of type `Numpy Float64` and length 441 (21 ^ 2)
	"""
	if landmarks.shape != (21, 3):
		return "Error!"

	connections = map(lambda t: landmarks[t[1]] - [t[0]], HAND_CONNECTIONS)

	angles_list = []
	for connection in product(connections, repeat=2):
		angle = _get_angle_between_connections(u=connection[0], v=connection[1])

		angles_list.append(angle if (angle == angle) else 0)

	return angles_list


def _get_angle_between_connections(u: np.ndarray, v: np.ndarray) -> np.float64:
	"""
	Calculates the Angle between a pair of Connections (A Connection is the direct Vector between two Keypoints) and returns it as a `Numpy Float64`

	Parameters
	----------
	u, v: `Numpy nD-Array`
		A 3D Vector representing a Connection

	Returns
	----------
	`Numpy Float64`
	"""
	if np.array_equal(u, v):
		return np.float64(0)

	dot_product = np.dot(a=u, b=v)
	norm = np.linalg.norm(x=u) * np.linalg.norm(x=v)

	return np.arccos(dot_product / norm)
