from email.mime import image
import io
from os import environ
from PIL import Image

import imageToText

from google.cloud import translate
from google.cloud import vision


class ImageToOutput:
    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()

        self.project_id = environ.get("PROJECT_ID", "")
        assert self.project_id

        self.vision_client = vision.ImageAnnotatorClient()
        self.word_areas = []  # 2D array containing wordRectanglePairs

        self.full_text = ""

    # Takes list of text, returns list of translations
    def __get_translation(self, text):
        parent = f"projects/{self.project_id}"

        response = self.translate_client.translate_text(
            contents=[text],
            target_language_code="fr",
            parent=parent,
        )

        return [translation.translated_text for translation in response.translations]

    def setup(self, pil_image):
        full_text_and_lines_array = imageToText.parse_image(
            self.vision_client, pil_image=pil_image
        )
        self.full_text = full_text_and_lines_array[0]
        self.word_areas = full_text_and_lines_array[1]

    def find_word(self, x, y):
        # Binary search by y-coordinate first
        low = 0
        mid = 0
        high = len(self.word_areas)
        while low <= high:
            mid = (high + low) // 2
            rectangle = self.word_areas[mid][0].rect
            comparisonRes = rectangle.inRangeY(y)
            if comparisonRes == 1:
                low = mid + 1
            elif comparisonRes == -1:
                high = mid - 1
            else:
                break

        line = self.word_areas[mid]
        low2 = 0
        mid2 = 0
        high2 = len(line) - 1
        while low2 <= high2:
            mid2 = (high2 + low2) // 2
            rectangle = line[mid2].rect
            comparisonRes = rectangle.inRangeX(x)
            if comparisonRes == 1:
                low2 = mid2 + 1
            elif comparisonRes == -1:
                high2 = mid2 - 1
            else:
                break

        return line[mid2].word

    def process(self, x, y):

        # Outputs word translated;
        pass


# (DAVID) TESTING:
# thing = ImageToOutput()
# thing.setup(Image.open("assets/sample_text_2.png"))
# print(thing.find_word(211, 320))
