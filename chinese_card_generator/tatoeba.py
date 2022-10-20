import requests
from dataclasses import dataclass
import hanzidentifier


@dataclass
class Sentence:
    chinese: str
    english: str


def get_sentence(word: str) -> Sentence:
    query = f'https://tatoeba.org/en/api_v0/search?from=cmn&query="{word}"&to=eng'
    response = requests.get(url=query)

    results = response.json()['results']
    for result in results:
        if hanzidentifier.is_simplified(result['text']):
            try:
                sentence = Sentence(
                    chinese=result['text'],
                    english=result['translations'][0][0]['text']
                )
                print(f"{word} - {sentence.chinese} - {sentence.english}")
                return sentence
            except IndexError:
                pass

    return Sentence(chinese='', english='')


if __name__ == '__main__':
    word = '下周'
    print(get_sentence(word=word))
