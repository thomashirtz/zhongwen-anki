from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from zhongwen_anki.utilities import get_marked_characters, Content
from deep_translator import GoogleTranslator
from pinyin import get as get_pinyin


@dataclass
class Synonyms:
    summary: str
    summary_colored: str


class SynonymsFinder(ABC):
    def __init__(self, n: int):
        self.n = n
        self.translator = None
    
    @abstractmethod
    def __call__(self, word: str) -> Synonyms:
        ...
    
    def _process(self, raw_synonym_list) -> Synonyms:
        synonym_list = []
        for synonym in raw_synonym_list[:self.n]:
            synonym_list.append(
                Content(
                    chinese=synonym,
                    english=self.translator.translate(synonym),
                    pinyin=get_pinyin(synonym),
                    chinese_colored=get_marked_characters(synonym),
                )
            )

        summary_list = []
        summary_list_colored = []
        for s in synonym_list:
            summary_list.append(
                f'{s.chinese} ({s.pinyin}) - {s.english}'
            )
            summary_list_colored.append(
                f'{s.chinese_colored} ({s.pinyin}) - {s.english}'
            )

        return Synonyms(
            summary='<br>'.join(summary_list if summary_list else []),
            summary_colored='<br>'.join(summary_list_colored if summary_list_colored else []),
        )


class EmptySynonymsFinder(SynonymsFinder):
    def __call__(self, word: str) -> Synonyms:
        return Synonyms(summary='', summary_colored='')


class CidianSynonymsFinder(SynonymsFinder):
    def __init__(self, n: int = 3):
        self.n = n
        self.translator = GoogleTranslator(source='zh-CN', target='en')

    def __call__(self, word: str) -> Synonyms:
        query = fr'https://cidian.qianp.com/ci/{word}'
        try:
            response = requests.get(url=query, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(response.content, 'html.parser')
            synonym = soup.findAll(class_='attr')[2].text[2:]
            raw_synonym_list = [w for w in synonym.split(' ') if w]
            return self._process(raw_synonym_list)
        except IndexError as e:  # IndexError => 404
            print('cidian', e)
            return Synonyms(summary='', summary_colored='')


class BaiduSynonymsFinder(SynonymsFinder):
    def __init__(self, n: int = 3):
        self.n = n
        self.translator = GoogleTranslator(source='zh-CN', target='en')

    def __call__(self, word: str) -> Synonyms:
        query = fr'https://hanyu.baidu.com/s?wd={word}同义词'
        try:
            response = requests.get(url=query, headers={'User-Agent': 'Custom'})
            soup = BeautifulSoup(response.content, 'html.parser')
            container = soup.find(class_='poem-list-container')

            raw_synonym_list = []
            for result in container.findAll(class_="check-red"):
                if 'poem-list-item-body' in result.attrs['class']:
                    continue
                raw_synonym_list.append(result.text.strip())
            return self._process(raw_synonym_list)
        except AttributeError as e:  # IndexError => 404
            print('cidian', e)
            return Synonyms(summary='', summary_colored='')


if __name__ == '__main__':
    word = '回答'
    sf = BaiduSynonymsFinder()
    sentence = sf(word)
    print(sentence)
    print()