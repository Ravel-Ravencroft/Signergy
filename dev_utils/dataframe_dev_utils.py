import cv2
import uuid

import pandas as pd
import pickle as pkl

from mediapipe.python.solutions.holistic import Holistic

from dev_utils.common_dev_params import Status, DATA_DIR, SIGNS_DIR, TRIMS_DIR
from utils import dataframe_utils as dtfm, landmark_utils as lnmk


DF_D_TYPES = {
	"sign": "category",
	"hand": "category",
}


# TODO: Convert Prints to Logs
def _process_video(video_name: str, model: Holistic) -> Status:
	landmark_lists = {"left": [], "right": []}
	sub_folder_path = f"{video_name.split('-')[0]}/{video_name}"

	try:
		cap = cv2.VideoCapture(str(TRIMS_DIR / f"{sub_folder_path}.mp4"))

		while cap.isOpened():
			has_frame, frame = cap.read()

			if (not has_frame):
				break

			{
				landmark_lists[hand].append(angles)
				for hand, angles in lnmk.extract_all_angles(
					detections=lnmk.detect_landmarks(image=frame, model=model)
				).items()
			}

		cap.release()

		dst_dir = SIGNS_DIR / sub_folder_path
		dst_dir.mkdir(parents=True, exist_ok=True)

		for hand, list in landmark_lists.items():
			with open(file=(dst_dir / f"{video_name}_{hand}.pkl"), mode="wb") as file:
				pkl.dump(obj=list, file=file)

		print(f"Extracted Landmarks from `{video_name}` Sign Video and Placed in `{sub_folder_path}`!")
		return Status.COMPLETE

	except Exception as e:
		print(f"An Error Occured while Processing Sign Video `{video_name}`:\n\n{e}")
		return Status.FAILED


# TODO: Convert Prints to Logs
def process_data(model: Holistic) -> Status:
	if (not TRIMS_DIR.is_dir()):
		print(f"The Source Directory `{TRIMS_DIR.parent.name}/{TRIMS_DIR.name}` Does Not Exist!")
		return Status.MISSING

	trims = {file.name.removesuffix(".mp4") for file in TRIMS_DIR.rglob("*.mp4")}

	if (not trims):
		print(f"The Source Directory `{TRIMS_DIR.parent.name}/{TRIMS_DIR.name}` is Empty!")
		return Status.EMPTY

	signs = {file.name for file in SIGNS_DIR.rglob("*/*/**")}

	new_files = trims.difference(signs)

	if (not new_files):
		print("No New Files to Process!")
		return Status.EXISTS

	file_count = len(new_files)
	print(f"Extracting Landmarks from New Files: {file_count} Files Detected!")

	{
		print(f"{idx}/{file_count}: {_process_video(video_name=file, model=model)}")
		for idx, file in enumerate(new_files, start=1)
	}

	return Status.COMPLETE


def _load_pickle(file_path: str) -> list:
	with open(file=file_path, mode="rb") as file:
		return pkl.load(file=file)


# TODO: Convert Prints to Logs
def create_dataframe(overwrite: bool = False) -> Status:
	if ((DATA_DIR / "dataset.pkl").is_file() and not overwrite):
		print(f"Dataset Pickle Already Exists!")
		return Status.EXISTS

	dataset = [
		{
			"file_name": file.name,
			"sign": file.parent.name,
			"left": _load_pickle(file_path=(file / f"{file.name}_left.pkl")),
			"right": _load_pickle(file_path=(file / f"{file.name}_right.pkl")),
			"hand": ""
		}
		for file in SIGNS_DIR.rglob("*/*/**")
	]

	for item in dataset:
		if (not (hand := dtfm.map_hands(hand_vector=(item["left"], item["right"])))):
			continue

		item["hand"] = hand.value

	pd.DataFrame.from_records(dataset).astype(DF_D_TYPES).to_pickle(DATA_DIR / "dataset.pkl")

	print("Dataset Pickle Created!")
	return Status.COMPLETE


# TODO: Convert Prints to Logs
def create_sign_dataframes(overwrite: bool = False) -> Status:
	write = False

	for sign in SIGNS_DIR.glob("*"):
		if ((sign / f"{sign.name}.pkl").is_file() and not overwrite):
			print(f"{sign.name} Dataset Pickle Already Exists!")
			continue

		dataset = [
			{
				"file_name": file.name,
				"sign": file.parent.name,
				"left": _load_pickle(file_path=(file / f"{file.name}_left.pkl")),
				"right": _load_pickle(file_path=(file / f"{file.name}_right.pkl")),
				"hand": ""
			}
			for file in sign.rglob("*/**")
		]

		for item in dataset:
			if (not (hand := dtfm.map_hands(hand_vector=(item["left"], item["right"])))):
				hand = ""
			item["hand"] = hand.value

		pd.DataFrame.from_records(dataset).astype(DF_D_TYPES).to_pickle(sign / f"{sign.name}.pkl")

		print(f"{sign.name} Dataset Pickle Created!")

		write = True

	return Status.COMPLETE if write else Status.EXISTS


# TODO: Convert Prints to Logs
def create_custom_dataframe(
	name: str = None, signs: list[str] = None, per_sign_count: int = None, overwrite: bool = False
) -> Status:
	if (not signs and not per_sign_count):
		print(f"Please Specify Either a Sign List or a Per-Sign-Max-Count to Use this Functionality!")
		return Status.MISSING

	if (name and (DATA_DIR / f"{name}.pkl").is_file() and not overwrite):
		print(f"`{name}` Dataset Pickle Already Exists!")
		return Status.EXISTS

	try:
		if (signs and per_sign_count):
			sign_library = pd.concat([
				pd.read_pickle(df)[:per_sign_count] for df in SIGNS_DIR.glob("*/*.pkl") if df.name.removesuffix(".pkl") in signs
			], ignore_index=True)

		if (signs and not per_sign_count):
			sign_library: pd.DataFrame = pd.read_pickle(DATA_DIR / "dataset.pkl")
			sign_library = sign_library[sign_library.sign.isin(values=signs)]

		if (per_sign_count and not signs):
			sign_library = pd.concat([
				pd.read_pickle(df)[:per_sign_count] for df in SIGNS_DIR.glob("*/*.pkl")
			], ignore_index=True)

		df_name = name if name else f"custom_dataset_{uuid.uuid4()}"
		pd.DataFrame.from_records(sign_library).astype(DF_D_TYPES).to_pickle(DATA_DIR / f"{df_name}.pkl")

		print(f"`{df_name}` Dataset Pickle Created!")
		return Status.COMPLETE

	except Exception as e:
		print(f"An Error Occured while Creating `{df_name}` Dataset Pickle:\n\n{e}")
		return Status.FAILED
