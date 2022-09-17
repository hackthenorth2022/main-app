import io
from os import environ
from PIL import Image

from google.cloud import translate
from google.cloud import vision

# Convert Image object (PIL) to bytes - so we can access the image in-memory
#   and don't need to store the Image object in a file.
def pilToBytes(pilImage):
    buffer = io.BytesIO()
    pilImage.save(buffer, format="PNG")
    return buffer.getvalue()
    
class ImageToOutput:
    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()
        self.project_id = environ.get("PROJECT_ID", "")
        assert self.project_id
        self.vision_client = ''
        self.word_areas = {} 

    # Takes list of text, returns list of translations
    def __get_translation(self, text):
        parent = f"projects/{self.project_id}"

        response = self.translate_client.translate_text(
        contents=[text],
        target_language_code='fr',
        parent=parent,)
        
        return [translation.translated_text for translation in response.translations]

    def parse_image(self, pil_image):
        pngBytes = pilToBytes(pil_image)

        # TEMP: Double check we got the bytes for the PNG
        print(pngBytes[:20])

        # GCP code
        client = vision.ImageAnnotatorClient()

        gcpImage = vision.Image(content=pngBytes)
        response = client.text_detection(image=gcpImage)
        boundedTexts = response.text_annotations

        return boundedTexts
    
    def setup(self, image):
        pass

    def process(self, coordinates):

        #Outputs word translated;
        pass

output = ImageToOutput()
print(output.parse_image(Image.open("assets/sample_text_1.png")))