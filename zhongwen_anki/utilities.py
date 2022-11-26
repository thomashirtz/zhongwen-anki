from zhongwen_anki.constants import tone_to_vowel_list
from pinyin import get as get_pinyin
from typing import Optional
from typing import List
from dataclasses import dataclass


@dataclass
class Content:
    chinese: str
    english: str
    pinyin: str
    chinese_colored: str


def add_mark(string: str, mark: str) -> str:
    # https://stackoverflow.com/questions/4622808/html-changing-colors-of-specific-words-in-a-string-of-text
    return f'<mark class="{mark}">{string}</mark>'


def contains(string: str, substring_list: List[str]) -> bool:
    return bool([s for s in substring_list if (s in string)])


def get_marked_characters(characters: str, pinyin: Optional[str] = None):

    character_list = list(characters)
    if pinyin is None:
        pinyin_list = [get_pinyin(c) for c in character_list]
    else:
        pinyin_list = pinyin.split(' ')

    marked_characters = ''
    for c, p in zip(character_list, pinyin_list):
        character = c
        for tone, vowel_list in tone_to_vowel_list.items():
            if contains(p, vowel_list):
                character = add_mark(c, tone)
                break
        marked_characters += character

    return ''.join(marked_characters)


if __name__ == '__main__':
    characters = '全球定位系统'
    pinyin = 'quán qiú dìng wèi xì tǒng'
    result = get_marked_characters(characters)
    print(pinyin)
    print(result)
