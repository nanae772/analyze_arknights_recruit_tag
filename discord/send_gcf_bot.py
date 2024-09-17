"""
ユーザーからDMで画像を受け取り、その画像をGoogle Cloud FunctionにHTTPリクエストで送信
"""
import base64
from logging import getLogger, StreamHandler, DEBUG
import requests
import yaml
import discord

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# 環境変数の読み込み
with open('.env.yaml', encoding='utf-8') as f:
    env = yaml.safe_load(f)


@bot.event
async def on_ready():
    logger.debug('Logged in as %s', bot.user)


@bot.event
async def on_message(message):
    logger.debug(message.attachments)
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('png', 'jpg', 'jpeg')):
                image_url = attachment.url
                logger.debug(image_url)
                send_image_to_gcf(image_url)


def send_image_to_gcf(image_url: str):
    """ Google Cloud FunctionのエンドポイントにHTTPリクエストで画像を送信 """
    endpoint = env['GCF_ENDPOINT']
    res = requests.get(image_url, timeout=10)
    data = {'image': base64.b64encode(res.content).decode()}
    response = requests.post(endpoint, json=data, timeout=10)
    if response.status_code == 200:
        logger.info('画像が正常に送信されました')
    else:
        logger.info('エラーが発生しました: %s', response.status_code)


bot.run(env['DISCORD_BOT_TOKEN'])
