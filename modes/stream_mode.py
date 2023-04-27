import cv2
import pyvirtualcam

from keras import Sequential
from mediapipe.python.solution_base import SolutionBase
from sklearn.preprocessing import LabelEncoder

from modes.common_mode_params import COLOUR
from utils import camera_utils, io_utils, landmark_utils, model_utils


def instantiate(
	model: Sequential,
	mediapipe: SolutionBase,
	label_encoder: LabelEncoder,
	settings: dict[str, int],
):
	frame_counter = 0
	is_recording = True
	landmark_lists = {"left": [], "right": []}
	text = ""

	dims = io_utils.get_camera_dimensions(settings["cam_src"])
	cap = cv2.VideoCapture(settings["cam_src"])

	with pyvirtualcam.Camera(**dims) as cam:
		while cap.isOpened():
			_, frame = cap.read()

			landmarks = landmark_utils.detect_landmarks(image=frame, model=mediapipe)

			camera_utils.draw_landmarks(image=frame, landmarks=landmarks)

			cv2.circle(
				img=frame,
				center=(30, 30),
				radius=20,
				color=COLOUR[is_recording],
				thickness=-1,
			)

			frame = cv2.flip(frame, 1)
			frame = camera_utils.add_text(image=frame, text=text)

			frame = cv2.resize(frame, (dims["width"], dims["height"]), interpolation=cv2.INTER_AREA)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

			frame_counter += 1

			if is_recording and (frame_counter < settings["sign_duration"]):
				{
					landmark_lists[hand].append(angles)
					for hand, angles in landmark_utils.extract_all_angles(
						detections=landmarks
					).items()
				}
				continue

			if is_recording and (frame_counter == settings["sign_duration"]):
				frame_counter = 0
				is_recording = False
				text = model_utils.infer_sign(
					landmarks=landmark_lists,
					model=model,
					lbl_enc=label_encoder,
					max_size=settings["max_size"],
				)
				{item.clear() for item in landmark_lists.values()}
				continue

			if not is_recording and (frame_counter == settings["gap_duration"]):
				frame_counter = 0
				is_recording = True
				text = ""
				continue

			cam.send(frame)
			cam.sleep_until_next_frame()

	cap.release()
