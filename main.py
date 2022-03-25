import pathlib
import requests
import time


class SuperHero:
    url = ' https://superheroapi.com/api/2619421814940190/'

    def __init__(self, name):
        self.name = name
        self.id = ''
        self.intelligence = ''

    def get_id(self):
        self.id = requests.get(self.url+'/search/'+self.name).json()['results'][0]['id']
        return self.id

    def get_intelligence(self):
        if not self.id:
            self.get_id()
        self.intelligence = requests.get(self.url+'/'+self.id+'/powerstats').json()['intelligence']
        return self.intelligence


def most_intelligence(heroes):
    for hero in heroes:
        if not hero.intelligence:
            hero.get_intelligence()
    intelligence_list = sorted(heroes, key=lambda hero: hero.intelligence)
    return intelligence_list[0]


class YaUploader:
    token = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def upload(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': 'disk:/'+self.file_path.name,
                  'overwrite': 'true'}
        upload_link = requests.get(url, headers=headers, params=params).json()['href']
        res = requests.put(upload_link, data=open(self.file_path, 'rb'))
        res.raise_for_status()
        if res.status_code == 201:
            return 'Файл  загружен'
        return 'Ошибка загрузки'


def stackoverflow():
    url = 'https://api.stackexchange.com/2.3/questions'
    to_date = int(time.time())
    from_date = (to_date-172800)
    params = {'fromdate': f'{from_date}',
              'todate': f'{to_date}',
              'tagged': 'python',
              'site': 'stackoverflow'}
    response = requests.get(url, params=params)
    data = response.json()["items"]
    for ids in data:
        print(ids['title'])


# однако, топорно))


if __name__ == '__main__':
    stackoverflow()
    print('-----------------')
    SuperHeroes = [SuperHero('Hulk'),
                   SuperHero('Captain America'),
                   SuperHero('Thanos')]
    winner = most_intelligence(SuperHeroes)
    print(f"Самый умный супергерой - {winner.name},  интеллект  {winner.intelligence}")
    print('-----------------')
    uploader = YaUploader(pathlib.Path('upload', 'test.txt'))
    print(uploader.upload())
