from PIL import Image
from google.cloud import vision
import io
from utils import rectangle, word_rectangle_pair

sampleImage = Image.open("assets/sample_text_2.png")

# Convert Image object (PIL) to bytes - so we can access the image in-memory
#   and don't need to store the Image object in a file.
def __pil_to_bytes(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


# Input: Image object (PIL) to be passed in from Samantha's app.
# Output: [string of all text in the image, 2D array containing wordRectanglePairs]
def parse_image(client, pil_image=sampleImage):
    pngBytes = __pil_to_bytes(pil_image)

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
                word_rectangle_pair.WordRectanglePair(word, rect)
            )

    return [full_text, lines_array]

    # Testing correctness
    # for line in lines_array:
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
