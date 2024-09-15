import base64
from google.cloud import vision


def detect_text(request):
    request_json = request.get_json(silent=True)
    if request_json and 'image' in request_json:
        image_data = base64.b64decode(request_json['image'])

        # Cloud Vision APIでテキスト抽出
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        return texts[0].description
    else:
        return 'Error'
