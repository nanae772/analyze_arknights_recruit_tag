import base64
from google.cloud import vision
from tag_to_operators_mapper import obtain_result_message, get_tag_list


def detect_text(request):
    request_json = request.get_json(silent=True)
    if request_json and 'image' in request_json:
        image_data = base64.b64decode(request_json['image'])

        # Cloud Vision APIでテキスト抽出
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        tag_list = get_tag_list(texts)
        result_message = obtain_result_message(tag_list)

        return result_message
    else:
        return 'Error'
