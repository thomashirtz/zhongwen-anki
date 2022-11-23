from abc import abstractmethod

import requests
from dataclasses import dataclass
import pinyin

from bs4 import BeautifulSoup
from zhongwen_anki.utilities import get_marked_characters
from abc import ABC
from deep_translator import GoogleTranslator


@dataclass
class Meaning:
    chinese: str
    english: str
    pinyin: str
    chinese_colored: str


class MeaningFinder(ABC):
    """Abstract class to define the sentence finder interface."""
    @abstractmethod
    def __call__(self, word: str) -> Meaning:
        """Method used to find a "Sentence" example using a word.

        Args:
            word: String containing the word.

        Returns:
            `Sentence` object.
        """


class EmptyMeaningFinder(MeaningFinder):
    def __call__(self, word: str) -> Meaning:
        return Meaning(chinese='', english='', pinyin='', chinese_colored='')


class CidianMeaningFinder(MeaningFinder):
    def __init__(self):
        self.translator = GoogleTranslator(source='zh-CN', target='en')

    def __call__(self, word: str) -> Meaning:
        query = fr'https://cidian.qianp.com/ci/{word}'
        try:
            response = requests.get(url=query, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(response.content, 'html.parser')
            meaning = soup.find(class_='indent').text[3:]
            return Meaning(
                chinese=meaning,
                english=self.translator.translate(meaning),
                pinyin=pinyin.get(meaning),
                chinese_colored=get_marked_characters(meaning),
            )
        except AttributeError as e: #attr => 404
            print('cidiane', e)
            return Meaning(
                chinese='',
                english='',
                pinyin='',
                chinese_colored=''
            )


if __name__ == '__main__':
    word = '教化'
    mf = CidianMeaningFinder()
    meaning = mf(word)
    print(meaning)
    print()
