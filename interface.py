from dotenv import load_dotenv
load_dotenv()

from email.mime import image
import io
from os import environ
from PIL import Image
from utils import rectangle, word_rectangle_pair


from google.cloud import translate
from google.cloud import vision
# from PyDictionary import PyDictionary

import wordToSentence


class ImageToOutput:
    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()

        self.project_id = environ.get("GOOGLE_PROJECT_ID", "")
        assert self.project_id

        self.vision_client = vision.ImageAnnotatorClient()
        self.word_areas = []  # 2D array containing wordRectanglePairs

        self.full_text = ""

    # def __get_definition(self, word):
    #     return PyDictionary.meaning(word)

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
        full_text_and_lines_array = self.parse_image(pil_image=pil_image)
        self.full_text = full_text_and_lines_array[0]
        self.word_areas = full_text_and_lines_array[1]

    # Return the word at the coordinates, as well as the column and row.
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

        return line[mid2].word, mid, mid2

    def process(self, x, y, process_type="translate"):
        word, column, row = self.find_word(x, y)
        # if process_type == "definition":
        #     processedWord = self.__get_definition(word)
        # else:
        print("non-translated is: "+word)
        processedWord = self.__get_translation(word)[0]
        return processedWord, column, row

    sampleImage = Image.open("assets/sample_text_3.png")

    


    # Input: Image object (PIL) to be passed in from Samantha's app.
    # Output: [string of all text in the image, 2D array containing wordRectanglePairs]
    def parse_image(self, pil_image=sampleImage):
        client = self.vision_client
        # Convert Image object (PIL) to bytes - so we can access the image in-memory
        #   and don't need to store the Image object in a file.
        def pil_to_bytes(pil_image):
            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")
            return buffer.getvalue()

        pngBytes = pil_to_bytes(pil_image)

        # GCP code
        gcpImage = vision.Image(content=pngBytes)
        response = client.text_detection(image=gcpImage)

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        texts = response.text_annotations

        # Grab all text from the image
        full_text = response.text_annotations[0].description
        texts.pop(0)

        # Put each individual word into data structure
        lines_array = []  # array of array of word-rectangle pairs, sorted by y-coord.
        word_rectangle_pairs = []  # array of word-rectangle pairs, sorted by x-coord.

        for textObj in texts:
            word = textObj.description
            rect = rectangle.Rectangle(
                textObj.bounding_poly.vertices[0], textObj.bounding_poly.vertices[2]
            )

            if word.isalpha():
                if word_rectangle_pairs and not rect.sameRectangleY(
                    word_rectangle_pairs[0].rect
                ):
                    lines_array.append(word_rectangle_pairs)
                    word_rectangle_pairs = []

                word_rectangle_pairs.append(
                    word_rectangle_pair.WordRectanglePair(word, rect, self.__get_translation(word)[0])
                )

        # # Testing correctness
        # for line in lines_array:
        #     print("--------------------")
        #     for wordRectanglePair in line:
        #         # print("Word: {}".format(wordRectanglePair.word))
        #         print(
        #             "Word: {}\nMinX: {} MaxX: {} MinY: {} MaxY: {}".format(
        #                 wordRectanglePair.word,
        #                 wordRectanglePair.rect.minX,
        #                 wordRectanglePair.rect.maxX,
        #                 wordRectanglePair.rect.minY,
        #                 wordRectanglePair.rect.maxY,
        #             )
        #         )

        return [full_text, lines_array]

    # (DAVID) TESTING:
thing = ImageToOutput()
thing.setup(Image.open("assets/sample_text_3.png"))
# thing.word_areas
# len(self.word_areas)
for i in range(len(thing.word_areas)):
    for j in range(len(thing.word_areas[0])):
        print(thing.word_areas[i][j])


processedWord, column, row = thing.process(211, 320)
print(processedWord)
    # processedWord2, column2, row2 = thing.process(300, 100)
    # print(processedWord2)


# Testing:
# output = ImageToOutput()
# print(output.get_defintion("moist"))

# print(wordToSentence.wordToSentence("", column, row, thing.word_areas))
# print("-----")
# print(thing.full_text)
