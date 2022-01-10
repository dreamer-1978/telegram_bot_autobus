from bs4 import BeautifulSoup
import requests

URL_AUTOBUS = 'https://yandex.ru/maps/213/moscow/stops/stop__9643717/?ll=37.829003%2C55.777361&tab=overview&z=16.29'


class Parser:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        req = requests.get(self.url)
        if req.status_code == 200:
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


def main():
    parser = Parser(URL_AUTOBUS)
    parser.parser_content()
    cont = parser.open_content()

    parser.erase_content()


if __name__ == '__main__':
    main()
