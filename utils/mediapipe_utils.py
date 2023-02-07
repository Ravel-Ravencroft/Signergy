import cv2
import numpy as np

from mediapipe.python.solutions.holistic import Holistic


def detect_landmarks(image: np.ndarray, model: Holistic):
    image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
    image.setflags(write=False)
    return model.process(image=image)
