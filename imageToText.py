from PIL import Image
from google.cloud import vision
import io

# TEMP: Replace with Image object from Samantha (PIL)
pilImage = Image.new("RGB", (320, 240), (255, 0, 0))

# Create in-memory PNG - like you want for Google Cloud Vision
buffer = io.BytesIO()
pilImage.save(buffer, format="PNG")

pngBytes = buffer.getvalue()

# TEMP: Replace with GCP API call
print(pngBytes[:20])

# GCP code
client = vision.ImageAnnotatorClient()

gcpImage = vision.Image(content=pngBytes)
response = client.text_detection(image=gcpImage)
texts = response.text_annotations

for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = [
        "({},{})".format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices
    ]

    print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
