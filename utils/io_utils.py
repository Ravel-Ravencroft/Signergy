import cv2


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
