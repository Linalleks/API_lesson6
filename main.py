from pathlib import Path
import random

from decouple import config
import requests
import telegram


def download_image(image_url, download_path):
    response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; HandsomeBrowser/1.2)'})
    response.raise_for_status()
    image = Path(download_path)
    image.write_bytes(response.content)


def main():
    bot = telegram.Bot(token=config('TG_BOT_TOKEN'))
    channel_id = config('TG_CHANNEL_ID')

    last_comics = requests.get('https://xkcd.com/info.0.json')
    last_comics.raise_for_status()
    comics_total = last_comics.json()["num"]

    random_comics_id = random.randint(1, comics_total)
    random_comics = requests.get(f'https://xkcd.com/{random_comics_id}/info.0.json')
    random_comics.raise_for_status()
    image_url = random_comics.json()["img"]
    comics_title = random_comics.json()["title"]
    comics_comment = random_comics.json()["alt"]
    comics_download_path = f'{comics_title}{Path(image_url).suffix}'
    download_image(image_url, comics_download_path)

    comics = Path(comics_download_path)
    bot.send_photo(chat_id=channel_id, photo=comics.read_bytes(), caption=comics_comment)
    comics.unlink()


if __name__ == '__main__':
    main()
