import ffmpeg
import json

from dev_utils.common_dev_params import Status, RAWS_DIR, TRIMS_DIR


# TODO: Convert Prints to Logs
def _trim_video(
	video_id: str, category: str, start_frame: int, end_frame: int
) -> Status:
	if (not (input_file := RAWS_DIR / f"{video_id}.mp4").exists()):
		print(f"Input File '{input_file.name}' Doesn't Exist in the `data/raw_data` Directory!")
		return Status.MISSING

	if ((output_file := TRIMS_DIR / f"{category}/{category}-{video_id}.mp4").is_file()):
		print(f"Output File '{output_file.name}' Already Exists in the `data/trimmed_videos/{output_file.parent.name}` Directory!!")
		return Status.EXISTS

	if (not (output_dir := TRIMS_DIR / f"{category}").is_dir()):
		output_dir.mkdir(parents=True, exist_ok=True)

	try:
		(
			ffmpeg.input(input_file)
			.trim(start_frame=start_frame, end_frame=end_frame)
			.setpts("PTS-STARTPTS")
			.output(str(output_file))
			.run(quiet=True)
		)

		print(f"Input File `{input_file.name}` has been Trimmed and Placed in the `data/trimmed_videos/{output_file.parent.name}` Directory as {output_file.name}!")
		return Status.COMPLETE

	except Exception as e:
		print(f"An Error Occured while Trimming `{input_file.name}` for `{output_file.name}`:\n\n{e}")
		return Status.FAILED


# TODO: Convert Prints to Logs
def ingest_files() -> Status:
	if (not RAWS_DIR.is_dir()):
		print("Source Directory Doesn't Exist!")
		return Status.MISSING

	for file in RAWS_DIR.glob("*.json"):
		with open(file) as f:
			ingest_file = json.load(fp=f)

		length = len(ingest_file)

		{
			print(f"{idx}/{length}: \t{_trim_video(**video)}")
			for idx, video in enumerate(ingest_file)
		}

	return Status.COMPLETE
