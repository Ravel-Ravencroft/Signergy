import json
import logging
import pickle as pkl

from keras import models as krs
from keras import Sequential
from mediapipe.python.solutions.holistic import Holistic
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

from modes import practice_mode, stream_mode


ROOT_DIR = Path(__file__).parent.resolve()
DATA_DIR = ROOT_DIR / 'data'

LOG_LEVEL_TRANSLATION = {
	'critical': logging.CRITICAL,
	'debug': logging.DEBUG,
	'error': logging.ERROR,
	'info': logging.INFO,
	'warning': logging.WARNING,
}

with open(ROOT_DIR / 'config.json') as config:
	CONFIG = json.load(fp=config)

logging.basicConfig(
	level=LOG_LEVEL_TRANSLATION.get(CONFIG['log_level'], logging.ERROR),
	filename='log.log',
	filemode='w',
	format='%(created)f: %(name)s - %(levelname)s - %(message)s'
)

MEDIAPIPE = Holistic()


if (__name__ == '__main__'):
	MODEL: Sequential = krs.load_model(DATA_DIR / f'{CONFIG["model_name"]}.h5')

	with open(DATA_DIR / f'{CONFIG["encoder_name"]}.pkl', 'rb') as file:
		LBL_ENC: LabelEncoder = pkl.load(file)

	if (CONFIG['stream_mode']):
		stream_mode.instantiate(
			model=MODEL,
			mediapipe=MEDIAPIPE,
			label_encoder=LBL_ENC,
			settings=CONFIG['settings']
		)
	else:
		practice_mode.instantiate(
			model=MODEL,
			mediapipe=MEDIAPIPE,
			label_encoder=LBL_ENC,
			settings=CONFIG['settings']
		)
