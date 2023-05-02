import numpy as np

from keras import Sequential
from sklearn.preprocessing import LabelEncoder


def normalise_data(left: np.ndarray, right: np.ndarray, max_frames: int) -> np.ndarray:
	if len(left) < max_frames:
		increment = [np.zeros(shape=441) for _ in range(max_frames - len(left))]
		temp_1 = np.concatenate((left, increment), axis=0)
		temp_2 = np.concatenate((right, increment), axis=0)
		result = np.stack((temp_1, temp_2), axis=0)

	else:
		result = np.stack((left, right), axis=0)

	return result


def infer_sign(
	landmarks: dict[str, list[np.ndarray[np.float64]]],
	model: Sequential,
	lbl_enc: LabelEncoder,
	max_size: int,
) -> str:
	data = normalise_data(landmarks['left'], landmarks['right'], max_size)
	input_data = data.reshape((1,) + data.shape)

	return lbl_enc.inverse_transform([np.argmax(model.predict(x=input_data))])[0]
