import cv2

from mediapipe.python.solution_base import SolutionBase

from utils import camera_utils, landmark_utils


def instantiate(model: SolutionBase, cam_id: int = 0):
	cap = cv2.VideoCapture(cam_id)

	while cap.isOpened():
		_, frame = cap.read()

		landmarks = landmark_utils.detect_landmarks(image=frame, model=model)

		camera_utils.draw_landmarks(image=frame, landmarks=landmarks)

		frame = cv2.flip(frame, 1)

		cv2.imshow(winname="Practice Mode", mat=frame)

		pressed_key = cv2.waitKey(delay=1) & 0xFF

		if (pressed_key == ord("q")):
			cv2.destroyAllWindows()
			break

	cap.release()
