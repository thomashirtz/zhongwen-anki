import requests
from dataclasses import dataclass


@dataclass
class Sentence:
    chinese: str
    english: str


# todo fix bug sometime sentence can be traditional, e.g. 防弹衣 => 湯姆穿著一件防彈衣，所以子彈沒把他殺死。
def get_sentence(word: str) -> Sentence:
    query = f'https://tatoeba.org/en/api_v0/search?from=cmn&query="{word}"&to=eng'
    print(query)
    response = requests.get(url=query)
    results = response.json()['results']
    try:
        return Sentence(
            chinese=results[0]['text'],
            english=results[0]['translations'][0][0]['text']
        )
    except IndexError:
        return Sentence(chinese='', english='')


if __name__ == '__main__':
    word = '下周'
    print(get_sentence(word=word))
