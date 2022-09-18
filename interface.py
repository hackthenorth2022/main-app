from email.mime import image
import io
from os import environ
from PIL import Image

import imageToText

from google.cloud import translate
from google.cloud import vision
from PyDictionary import PyDictionary



class ImageToOutput:
    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()

        self.project_id = environ.get("PROJECT_ID", "")
        assert self.project_id

        self.vision_client = vision.ImageAnnotatorClient()
        self.word_areas = []  # 2D array containing wordRectanglePairs

        self.full_text = ""

    def get_defintion(self, word):
        return PyDictionary.meaning(word)

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

    def __find_word(self, x, y):
        return "hello"
        # # Binary search by y-coordinate first
        # low = 0
        # mid = 0
        # high = len(self.word_areas)
        # while low <= high:
        #     mid = (high + low) // 2
        #     rectangle = self.word_areas[mid][0].rect
        #     if s. < y:
        #         low = mid + 1
        #     elif self.word_areas[mid] > y:
        #         high = mid - 1
        #     else:
        #         break

        # line = self.word_areas[mid]
        # low2 = 0
        # mid2 = 0
        # high2 = len(line) - 1
        # while low2 <= high2:
        #     mid2 = (high2 + low2) // 2
        #     if line[mid] < x:
        #         low = mid + 1
        #     elif self.word_areas[mid] > y:
        #         high = mid - 1
        #     else:
        #         break

    def process(self, x, y):

        # Outputs word translated;
        pass


output = ImageToOutput()
print(output.get_defintion("moist"))
