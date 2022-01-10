from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json

app = Flask(__name__)
ssl_ify = SSLify(app)

TOKEN = '5075619990:AAEyF5W1D_JmFuN6y6BGp2lpxXupKyR0Ays'
URL = f'https://api.telegram.org/bot{TOKEN}/'
URL_AUTOBUS = 'https://yandex.ru/maps/213/moscow/stops/stop__9643717/?ll=37.829003%2C55.777361&tab=overview&z=16.29'


class Parser:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        req = requests.get(self.url)
        return req.text

    def parser_content(self):
        soup = BeautifulSoup(self.get_content(), 'lxml')
        block_content = soup.find('ul', class_='masstransit-brief-schedule-view__vehicles').find_all('li')
        for item in block_content:
            number_bus = item.find('a').text.strip()
            time_bus = item.find('span', class_='masstransit-prognoses-view__title-text').text.strip()

            content_bus = {number_bus: time_bus}
            self.save_content(content_bus)
            # return self.open_content()

    def save_content(self, data):
        with open('autobus.txt', 'a') as file:
            for key, val in data.items():
                file.write(f"{key}, {val}\n")

    def open_content(self):
        with open('autobus.txt') as file:
            cont_file = file.read().strip().replace(',', ' -')
            return cont_file

    def erase_content(self):
        with open('autobus.txt', 'w+') as file:
            file.seek(0)



web_hook = 'https://api.telegram.org/bot5075619990:AAEyF5W1D_JmFuN6y6BGp2lpxXupKyR0Ays/setWebhook?url=https://dreamer1978.pythonanywhere.com/'

def write_json(data, filename='update.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def send_message(chat_id, text='Serega Super Coder'):
    url = 'https://api.telegram.org/bot5075619990:AAEyF5W1D_JmFuN6y6BGp2lpxXupKyR0Ays/sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    req = requests.get(url, json=answer)
    return req.json()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if 'A' in message:
            parser = Parser(URL_AUTOBUS)
            parser.parser_content()
            content = parser.open_content()
            parser.erase_content()
            send_message(chat_id, text=content)
        # write_json(r)
        return jsonify(r)
    return f'<h1>Bot welcome you</h1>'


if __name__ == '__main__':
    app.run()
