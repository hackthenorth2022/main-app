from PIL import Image
from google.cloud import vision
import io
from utils import rectangle, word_rectangle_pair

sampleImage1 = Image.open("assets/sample_text_2.png")

# Convert Image object (PIL) to bytes - so we can access the image in-memory
#   and don't need to store the Image object in a file.
def pilToBytes(pilImage):
    buffer = io.BytesIO()
    pilImage.save(buffer, format="PNG")
    return buffer.getvalue()


# Input: Image object (PIL) to be passed in from Samantha's app.
# Output: [string of all text in the image, 2D array containing wordRectanglePairs]
def parseImage(pilImage=sampleImage1):
    pngBytes = pilToBytes(pilImage)

    # GCP code
    client = vision.ImageAnnotatorClient()  # TODO: Move into the class.

    gcpImage = vision.Image(content=pngBytes)
    response = client.text_detection(image=gcpImage)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    texts = response.text_annotations

    # Grab all text from the image
    fullText = response.text_annotations[0].description
    texts.pop(0)

    # Put each individual word into data structure
    linesArray = []  # array of array of word-rectangle pairs, sorted by y-coord.
    wordRectanglePairs = []  # array of word-rectangle pairs, sorted by x-coord.

    for textObj in texts:
        word = textObj.description
        rect = rectangle.Rectangle(
            textObj.bounding_poly.vertices[0], textObj.bounding_poly.vertices[2]
        )

        if word.isalpha():
            if wordRectanglePairs and not rect.sameRectangleY(
                wordRectanglePairs[0].rect
            ):
                linesArray.append(wordRectanglePairs)
                wordRectanglePairs = []

            wordRectanglePairs.append(word_rectangle_pair.WordRectanglePair(word, rect))

    return [fullText, linesArray]

    # Testing correctness
    # for line in linesArray:
    #     print("--------------------")
    #     for wordRectanglePair in line:
    #         print("Word: {}".format(wordRectanglePair.word))
    #         # print(
    #         #     "Word: {}\nMinX: {} MaxX: {} MinY: {} MaxY: {}".format(
    #         #         wordRectanglePair.word,
    #         #         wordRectanglePair.rect.minX,
    #         #         wordRectanglePair.rect.maxX,
    #         #         wordRectanglePair.rect.minY,
    #         #         wordRectanglePair.rect.maxY,
    #         #     )
    #         # )


parseImage()
