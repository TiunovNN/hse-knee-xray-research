import io

import catboost
import numpy as np
from PIL import Image
from skimage.feature import hog


class Predictor:
    def __init__(self, model: catboost.CatBoostClassifier):
        self.model = model

    @staticmethod
    def hog_picture(image: io.IOBase):
        image = Image.open(image).convert('L').resize((128, 128))
        array = np.asarray(image)
        vector = hog(
            array,
            orientations=9,
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2),
            feature_vector=True,
        )
        return vector

    def predict(self, image: io.IOBase) -> int:
        vector = self.hog_picture(image)
        severity = self.model.predict(vector)
        return severity[0]
