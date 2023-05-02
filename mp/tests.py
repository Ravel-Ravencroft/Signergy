import cv2
import numpy as np

from pathlib import Path

from mp import functionality


TEST_DIR = Path(__file__).parents[1].resolve() / "test_files"
ONE_HANDED_FILE = "test_one_hand"
TWO_HANDED_FILE = "test_two_hands"


def grab_frame(multi_handed: bool) -> None:
	cap = cv2.VideoCapture(str(TEST_DIR / f"{TWO_HANDED_FILE if multi_handed else ONE_HANDED_FILE}.mp4"))

	while cap.isOpened():
		has_frame, frame = cap.read()

		if (not has_frame):
			break

		np.save(
			file=(TEST_DIR / f"{TWO_HANDED_FILE if multi_handed else ONE_HANDED_FILE}.npy"), 
			arr=frame
		)


def test_detection_results(multi_handed: bool) -> None:
	frame = np.load(file=(TEST_DIR / f"{TWO_HANDED_FILE if multi_handed else ONE_HANDED_FILE}.npy"))
	results = functionality.detect_landmarks(frame)

	# print(f"""Results: 
	# Fields: {results._fields} 
	# Type: {type(results)}, 
	# Length: {len(results.__dict__)}
	# """)

	print(f"""Multi-Hand Landmarks: 
	Type: {type(results.multi_hand_landmarks)}, 
	Length: {len(results.multi_hand_landmarks)},
		Item Type: {type(results.multi_hand_landmarks[0])},
		Item Length: {sum(1 for _ in results.multi_hand_landmarks[0].landmark)},
		Items: {results.multi_hand_landmarks[0].landmark},
			Sub-Item Type: {type(results.multi_hand_landmarks[0].landmark[0])},
			Sub-Items: {results.multi_hand_landmarks[0].landmark[0]},
				Sub-Sub-Item Type: {type(results.multi_hand_landmarks[0].landmark[0].x)},
				Sub-Sub-Items: {results.multi_hand_landmarks[0].landmark[0].x}
	""")

	# print(f"""Multi-Hand World Landmarks: 
	# Type: {type(results.multi_hand_world_landmarks)}, 
	# Length: {len(results.multi_hand_world_landmarks)},
	# 	Item Type: {type(results.multi_hand_world_landmarks[0])},
	# 	Item Length: {sum(1 for _ in results.multi_hand_world_landmarks[0].landmark)},
	# 	Items: {results.multi_hand_world_landmarks[0].landmark},
	# 		Sub-Item Type: {type(results.multi_hand_world_landmarks[0].landmark[0])},
	# 		Sub-Items: {results.multi_hand_world_landmarks[0].landmark[0]},
	# 			Sub-Sub-Item Type: {type(results.multi_hand_world_landmarks[0].landmark[0].x)},
	# 			Sub-Sub-Items: {results.multi_hand_world_landmarks[0].landmark[0].x}
	# """)

	# print(f"""Multi-Handedness: 
	# Type: {type(results.multi_handedness)}, 
	# Length: {len(results.multi_handedness)},
	# Items: {results.multi_handedness},
	# 	Sub-Item Container Type: {type(results.multi_handedness[0])},
	# 	Sub-Items: {results.multi_handedness[0].classification}
	# 		Sub-Item One Type: {type(results.multi_handedness[0].classification[0].index)}
	# 		Sub-Item One: {results.multi_handedness[0].classification[0].index}\n
	# 		Sub-Item Two Type: {type(results.multi_handedness[0].classification[0].score)}
	# 		Sub-Item Two: {results.multi_handedness[0].classification[0].score}\n
	# 		Sub-Item Three Type: {type(results.multi_handedness[0].classification[0].label)}
	# 		Sub-Item Three: {results.multi_handedness[0].classification[0].label}
	# """)
