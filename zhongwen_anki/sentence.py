from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
import pinyin
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from zhongwen_anki.utilities import get_marked_characters


@dataclass
class Sentence:
    chinese: str
    english: str
    pinyin: str
    chinese_colored: str


class SentenceFinder(ABC):
    """Abstract class to define the sentence finder interface."""
    @abstractmethod
    def __call__(self, word: str) -> Sentence:
        """Method used to find a "Sentence" example using a word.

        Args:
            word: String containing the word.

        Returns:
            `Sentence` object.
        """


class EmptySentenceFinder(SentenceFinder):
    def __call__(self, word: str) -> Sentence:
        return Sentence(chinese='', english='', pinyin='')


class ZaixianSentenceFinder(SentenceFinder):
    def __init__(self):
        self.translator = GoogleTranslator(source='zh-CN', target='en')

    def __call__(self, word: str) -> Sentence:
        query = fr'http://www.87653.com/{word}造句/'
        try:
            response = requests.get(url=query, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(response.content, 'html.parser')
            if response.status_code == 404:
                return Sentence(
                    chinese='',
                    english='',
                    pinyin='',
                    chinese_colored=''
                )
            sentence = soup.find('p').text[2:]
            return Sentence(
                chinese=sentence,
                english=self.translator.translate(sentence),
                pinyin=pinyin.get(sentence),
                chinese_colored=get_marked_characters(sentence),
            )
        except Exception as e:
            print('cidiana', e)
            return Sentence(
                chinese='',
                english='',
                pinyin='',
                chinese_colored=''
            )


if __name__ == '__main__':
    word = '防弹衣'
    sf = ZaixianSentenceFinder()
    sentence = sf(word)
    print(sentence)
    print()