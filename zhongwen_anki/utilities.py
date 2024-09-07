import re

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
    if string == ' ':
        return ' '
    # https://stackoverflow.com/questions/4622808/html-changing-colors-of-specific-words-in-a-string-of-text
    return f'<mark class="{mark}">{string}</mark>'


def contains(string: str, substring_list: List[str]) -> bool:
    return bool([s for s in substring_list if (s in string)])


def is_chinese_character(char):
    """
    Check if a given character is a Chinese character (simplified or traditional).

    :param char: A single character to check.
    :return: True if the character is Chinese, False otherwise.
    """
    if len(char) != 1:
        raise ValueError("Input must be a single character")

    # Check for common Chinese character ranges in Unicode
    # CJK Unified Ideographs: U+4E00 to U+9FFF
    # CJK Unified Ideographs Extension A: U+3400 to U+4DBF
    # CJK Unified Ideographs Extension B to F: U+20000 to U+2FA1F
    # CJK Compatibility Ideographs: U+F900 to U+FAFF

    ranges = [
        ('\u4e00', '\u9fff'),
        ('\u3400', '\u4dbf'),
        ('\u20000', '\u2a6df'),
        ('\u2a700', '\u2b73f'),
        ('\u2b740', '\u2b81f'),
        ('\u2b820', '\u2ceaf'),
        ('\u2ceb0', '\u2ebef'),
        ('\uf900', '\ufaff'),
    ]
    return any(start <= char <= end for start, end in ranges)


def get_marked_characters(characters: str, pinyin: Optional[str] = None):

    character_list = list(characters)
    if pinyin is None:
        pinyin_list = [get_pinyin(c) if is_chinese_character(c) else None for c in character_list if c != '']
    else:
        pinyin_list = [p for p in pinyin.split(' ') if p != ' ' and p != '']

    marked_characters = ''
    for c, p in zip(character_list, pinyin_list):
        character = c
        if p is None:
            marked_characters += character
            continue
        for tone, vowel_list in tone_to_vowel_list.items():
            if contains(p, vowel_list):
                character = add_mark(c, tone)
                break
        marked_characters += character

    return ''.join(marked_characters)


def replace_extra_space(sentence: str): # todo ask chatgpt to make it better
    if not sentence:
        return ''
    output = ''
    for i in range(len(sentence) - 1): # todo something while empty space, do not add things
        if sentence[i] == ' ':
            if sentence[i+1] == ' ':
                output += ' '
        else:
            output += sentence[i]
    output += sentence[-1]
    return output




def process_synonyms(synonym_string: str) -> str:
    # Split the synonym string by <br> to get individual synonyms
    synonyms = synonym_string.split('<br>')

    # Regex pattern to extract characters and pinyin (e.g., '标量 (biāo liàng)')
    pattern = re.compile(r'([\u4e00-\u9fff]+)\s*\(([\w\s]+)\)\s*-\s*[\w\s]+')

    processed_synonyms = []

    for synonym in synonyms:
        match = pattern.search(synonym)
        if match:
            characters = match.group(1)  # Extracted characters
            pinyin = match.group(2)  # Extracted pinyin
            # Call the get_marked_characters function
            marked_characters = get_marked_characters(characters, pinyin)
            # Replace characters in the synonym with marked characters
            processed_synonym = synonym.replace(characters, marked_characters)
            processed_synonyms.append(processed_synonym)
        else:
            # If no match is found, keep the original synonym
            processed_synonyms.append(synonym)

    # Join processed synonyms back into a string with <br> separators
    return '<br>'.join(processed_synonyms)

if __name__ == '__main__':
    characters = '全球定位系统'
    pinyin = 'quán qiú dìng wèi xì tǒng'
    result = get_marked_characters(characters)
    print(pinyin)
    print(result)

    characters = '全球定位系统'
    pinyin = 'quán qiú  dìng wèi  xì tǒng'
    print(replace_extra_space(pinyin))