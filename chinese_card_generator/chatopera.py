import synonyms
from dataclasses import dataclass
from typing import List


@dataclass
class Synonym:
    word: str
    score: float


def get_synonym_list(
        word: str,
        n: int = 3,
        threshold: float = 0.8
) -> List[Synonym]:
    results = synonyms.nearby(word=word, size=n)
    lst = []
    for synonym, score in zip(*results):
        if score > threshold:
            lst.append(Synonym(word=synonym, score=score))
    return lst


def format_synonym_list(synonym_list: List[Synonym]) -> str:
    lst = []
    for synonym in synonym_list:
        lst.append(f'{synonym.word} ({synonym.score:.3f})')
    return '<br>'.join(lst)


if __name__ == '__main__':
    print(format_synonym_list(get_synonym_list("识别")))
    print("NOT_EXIST: ", synonyms.nearby("NOT_EXIST"))
