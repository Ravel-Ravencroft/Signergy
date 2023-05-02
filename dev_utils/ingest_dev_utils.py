import ffmpeg
import json
import logging

from dev_utils.common_dev_params import Status, RAWS_DIR, TRIMS_DIR


def _trim_video(
	video_id: str, category: str, start_frame: int, end_frame: int
) -> Status:
	if (not (input_file := RAWS_DIR / f'{video_id}.mp4').exists()):
		logging.error(msg=f"Input File `{input_file.name}` Doesn't Exist in the `data/raw_data` Directory!")
		return Status.MISSING

	if ((output_file := TRIMS_DIR / f'{category}/{category}-{video_id}.mp4').is_file()):
		logging.info(msg=
			f'''Output File '{output_file.name}' Already Exists in the 
			`data/trimmed_videos/{output_file.parent.name}` Directory!!'''
		)
		return Status.EXISTS

	if (not (output_dir := TRIMS_DIR / f'{category}').is_dir()):
		output_dir.mkdir(parents=True, exist_ok=True)

	try:
		(
			ffmpeg.input(input_file)
			.trim(start_frame=start_frame, end_frame=end_frame)
			.setpts('PTS-STARTPTS')
			.output(str(output_file))
			.run(quiet=True)
		)

		logging.info(msg=
		   f'''Input File `{input_file.name}` has been Trimmed and Placed in the 
			`data/trimmed_videos/{output_file.parent.name}` Directory as {output_file.name}!'''
		)
		return Status.COMPLETE

	except Exception as e:
		logging.error(f'An Error Occured while Trimming `{input_file.name}` for `{output_file.name}`:\n\n{e}')
		return Status.FAILED


def ingest_files() -> Status:
	if (not RAWS_DIR.is_dir()):
		logging.error(msg="Source Directory Doesn't Exist!")
		return Status.MISSING

	for file in RAWS_DIR.glob('*.json'):
		with open(file) as f:
			ingest_file = json.load(fp=f)

		{_trim_video(**video) for video in ingest_file}

	return Status.COMPLETE
