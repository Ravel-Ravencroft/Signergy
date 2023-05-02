import cv2

from keras import Sequential
from mediapipe.python.solution_base import SolutionBase
from sklearn.preprocessing import LabelEncoder

from modes.common_mode_params import COLOUR
from utils import camera_utils, model_utils, landmark_utils


def instantiate(
	model: Sequential,
	mediapipe: SolutionBase,
	label_encoder: LabelEncoder,
	settings: dict[str, int],
):
	frame_counter = 0
	is_recording = True
	landmark_lists = {'left': [], 'right': []}
	text = ''

	cap = cv2.VideoCapture(settings['cam_src'])

	while cap.isOpened():
		has_frame, frame = cap.read()

		if not has_frame:
			continue

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

		cv2.imshow(winname='Practice Mode', mat=frame)

		pressed_key = cv2.waitKey(delay=1) & 0xFF

		if pressed_key == ord('q'):
			cv2.destroyAllWindows()
			break

		frame_counter += 1

		if is_recording and (frame_counter < settings['max_size']):
			{
				landmark_lists[hand].append(angles)
				for hand, angles in landmark_utils.extract_all_angles(
					detections=landmarks
				).items()
			}
			continue

		if is_recording and (frame_counter == settings['max_size']):
			frame_counter = 0
			is_recording = False
			text = model_utils.infer_sign(
				landmarks=landmark_lists,
				model=model,
				lbl_enc=label_encoder,
				max_size=settings['max_size'],
			)
			{item.clear() for item in landmark_lists.values()}
			continue

		if not is_recording and (frame_counter == (settings['max_size']/2)):
			frame_counter = 0
			is_recording = True
			text = ''
			continue

	cap.release()
