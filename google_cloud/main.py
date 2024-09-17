"""
アークナイツの公開求人の画像をアップロードして、星４以上確定するタグの組合せをDiscordのWebhookに送る
"""
import base64
from logging import getLogger, StreamHandler, DEBUG
import json
import os
import requests
from google.cloud import vision
from tag_to_operators_mapper import obtain_result_message, get_tag_list

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def detect_text(request):
    request_json = request.get_json(silent=True)
    if request_json and 'image' in request_json:
        image_data = base64.b64decode(request_json['image'])

        # Cloud Vision APIでテキスト抽出
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_data)
        response = client.text_detection(
            image=image,
            image_context={"language_hints": ["ja"]}
        )
        texts = response.text_annotations[0].description

        logger.info(texts)

        tag_list = get_tag_list(texts)

        logger.info(tag_list)

        result_message = obtain_result_message(tag_list)
        send_content_to_discord_webhook(result_message)

        return 'Success'
    else:
        return 'Error'


class NotFoundDiscordWebhookUrl(Exception):
    """環境変数からdiscordのwebhook urlが取得できなかったときのエラー"""


def send_content_to_discord_webhook(content: str):
    """ content を指定の discord webhook に送る"""
    url = os.environ.get('DISCORD_WEBHOOK_URL')
    if url is None:
        raise NotFoundDiscordWebhookUrl('Cannot get DISCORD_WEBHOOK_URL')
    message = {
        "content": content,
        "username": "Google Cloud Bot"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        url,
        data=json.dumps(message),
        headers=headers,
        timeout=10
    )
    return f"Discord Webhook response: {response.status_code}"
