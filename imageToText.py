from PIL import Image
from google.cloud import vision
import io

sampleImage1 = Image.open("assets/sample_text_1.png")

# Convert Image object (PIL) to bytes - so we can access the image in-memory
#   and don't need to store the Image object in a file.
def pilToBytes(pilImage):
    buffer = io.BytesIO()
    pilImage.save(buffer, format="PNG")
    return buffer.getvalue()


# Input: Image object (PIL) to be passed in from Samantha's app.
# Output: Text contained within the image.
def convertImageToText(pilImage=sampleImage1):
    pngBytes = pilToBytes(pilImage)

    # TEMP: Double check we got the bytes for the PNG
    print(pngBytes[:20])

    # GCP code
    client = vision.ImageAnnotatorClient()

    gcpImage = vision.Image(content=pngBytes)
    response = client.text_detection(image=gcpImage)
    texts = response.text_annotations

    # TEMP: Check texts received from the response
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = [
            "({},{})".format(vertex.x, vertex.y)
            for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )


convertImageToText()
