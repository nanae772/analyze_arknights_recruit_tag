"""
ユーザーからDMで画像を受け取り、その画像をGoogle Cloud FunctionにHTTPリクエストで送信
"""
import base64
import requests
import yaml
import discord

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# 環境変数の読み込み
with open('.env.yaml', encoding='utf-8') as f:
    env = yaml.safe_load(f)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    print(message.attachments)
    if message.attachments:  # 画像が添付されているか確認
        for attachment in message.attachments:
            if attachment.filename.endswith(('png', 'jpg', 'jpeg')):
                # 画像のURLを取得
                image_url = attachment.url
                print(image_url)
                # 画像をGoogle Cloud Functionに送信
                send_image_to_gcf(image_url)


def send_image_to_gcf(image_url: str):
    """ Google Cloud FunctionのエンドポイントにHTTPリクエストで画像を送信 """
    endpoint = env['GCF_ENDPOINT']
    res = requests.get(image_url, timeout=10)
    data = {'image': base64.b64encode(res.content).decode()}
    response = requests.post(endpoint, json=data, timeout=10)
    if response.status_code == 200:
        print('画像が正常に送信されました')
    else:
        print(f'エラーが発生しました: {response.status_code}')


bot.run(env['DISCORD_BOT_TOKEN'])
