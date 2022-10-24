from abc import ABC

import synonyms
from deep_translator import GoogleTranslator
from pinyin import get as get_pinyin


class ChatOperaSynonymsFinder(ABC):
    def __init__(self, n: int = 3, threshold: float = 0.8):
        self.n = n
        self.threshold = threshold
        self.translator = GoogleTranslator(source='zh-CN', target='en')

    def __call__(self, word: str) -> str:
        results = synonyms.nearby(word=word, size=self.n+1)

        lst = []
        for synonym, score in zip(*results):
            if score > self.threshold:
                pinyin = get_pinyin(synonym)
                meaning = self.translator.translate(synonym)
                lst.append(f'{synonym} ({pinyin}) - {meaning} ({score:.3f})')

        # The first synonym is the word itself
        return '<br>'.join(lst[1:] if lst else [])


if __name__ == '__main__':
    print(ChatOperaSynonymsFinder()("识别"))
    print("NOT_EXIST: ", ChatOperaSynonymsFinder()("NOT_EXIST"))