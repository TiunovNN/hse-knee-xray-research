import io
from PIL import Image

class Predictor:
    def __init__(self, model):
        self.model = model

    def predict(self, image: io.IOBase) -> int:
        img = Image.open(image).convert('L')
        results = self.model.predict(source= img, device= 'cpu')
        for result in results:
            probs = result.probs
        return probs.top1
