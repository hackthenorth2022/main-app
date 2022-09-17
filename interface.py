from os import environ

from google.cloud import translate

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

    def __parse_image(self, pil_image):
        pass
    
    def setup(self, image):
        pass

    def process(self, coordinates):

        #Outputs word translated;
        pass

output = ImageToOutput()