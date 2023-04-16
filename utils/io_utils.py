import cv2
import screeninfo


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


def get_monitor_names() -> list[str]:
	return sorted([monitor.name for monitor in screeninfo.get_monitors()])


def get_screen_dimensions(monitor_name: str = None) -> dict[str, int]:
	for monitor in screeninfo.get_monitors():
		if (monitor_name and monitor.name == monitor_name):
			return {"width": monitor.width, "height": monitor.height}
		
		if (not monitor_name and monitor.is_primary):
			return {"width": monitor.width, "height": monitor.height}
