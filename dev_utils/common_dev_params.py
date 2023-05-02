from enum import Enum, auto
from pathlib import Path


class Status(Enum):
	COMPLETE = auto()
	EXISTS = auto()
	EMPTY = auto()
	FAILED = auto()
	MISSING = auto()


DATA_DIR = Path(__file__).parents[1].resolve() / 'data'
RAWS_DIR = DATA_DIR / 'raw_data'
SIGNS_DIR = DATA_DIR / 'sign_files'
TRIMS_DIR = DATA_DIR / 'trimmed_videos'

