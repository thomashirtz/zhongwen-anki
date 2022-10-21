import synonyms
from dataclasses import dataclass
from typing import List
from deep_translator import GoogleTranslator


@dataclass
class Synonym:
    word: str
    meaning: str
    score: float


def get_synonym_list(
        word: str,
        n: int = 3,
        threshold: float = 0.8,
) -> List[Synonym]:
    results = synonyms.nearby(word=word, size=n+1)
    translator = GoogleTranslator(source='zh-CN', target='en')

    lst = []
    for synonym, score in zip(*results):
        if score > threshold:
            lst.append(
                Synonym(
                    word=synonym,
                    meaning=translator.translate(synonym),
                    score=score,
                )
            )

    # The first synonym is the word itself
    return lst[1:] if lst else []


def format_synonym_list(synonym_list: List[Synonym]) -> str:
    lst = []
    for synonym in synonym_list:
        lst.append(f'{synonym.word} - {synonym.meaning} ({synonym.score:.3f})')
    return '<br>'.join(lst)


if __name__ == '__main__':
    print(format_synonym_list(get_synonym_list("识别")))
    print("NOT_EXIST: ", synonyms.nearby("NOT_EXIST"))
