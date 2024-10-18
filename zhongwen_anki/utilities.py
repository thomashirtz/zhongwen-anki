import re
from typing import Optional, List

from pinyin import get as get_pinyin

from zhongwen_anki.constants import tone_to_vowel_list


def add_mark(character: str, tone: str) -> str:
    """
    Wraps a Chinese character with a mark that represents its tone.

    Args:
        character (str): The Chinese character to be marked.
        tone (str): The tone class to be added as a mark.

    Returns:
        str: The character wrapped in an HTML <mark> tag with the tone class.
    """
    if character == ' ':
        return ' '  # Return space as-is
    return f'<mark class="{tone}">{character}</mark>'


def mark_character_with_tone(character: str, pinyin: str, tone_map: dict) -> str:
    """
    Marks a character with the appropriate tone based on the corresponding pinyin.

    Args:
        character (str): The character to be marked.
        pinyin (str): The corresponding pinyin, which contains tone-marked vowels.
        tone_map (dict): A dictionary mapping tones to lists of vowels.

    Returns:
        str: The marked character, or the character as-is if no tone is found.
    """
    for tone, vowels in tone_map.items():
        if contains(pinyin, vowels):
            return add_mark(character, tone)  # Mark the character with the identified tone
    return character  # If no tone is found, return the character as-is


def get_marked_characters(characters: str, pinyin: Optional[str] = None) -> str:
    """
    Adds HTML tone marks to Chinese characters based on their associated pinyin tones.

    Args:
        characters (str): The string of Chinese characters to mark.
        pinyin (Optional[str]): The corresponding pinyin for the characters.

    Returns:
        str: The characters wrapped with tone-specific HTML <mark> tags.
    """
    character_list = list(characters)

    # If no pinyin is provided, generate pinyin for each character
    if pinyin is None:
        pinyin_list = [get_pinyin(c) if is_chinese_character(c) else None for c in character_list if c != '']
    else:
        pinyin_list = split_by_single_and_double_spaces(pinyin)

    preprocessed_chars = introduce_spaces_to_characters(character_list, pinyin_list)

    marked_result = ""
    for char, pinyin in zip(preprocessed_chars, pinyin_list):
        marked_result += mark_character_with_tone(char, pinyin, tone_to_vowel_list)

    return marked_result


def contains(string: str, substring_list: List[str]) -> bool:
    """
    Checks if any of the substrings in the given list exist in the string.

    Args:
        string (str): The string to search within.
        substring_list (List[str]): List of substrings to check for.

    Returns:
        bool: True if any substring is found in the string, False otherwise.
    """
    return any(substring in string for substring in substring_list)


def is_chinese_character(char: str) -> bool:
    """
    Determines if a given character is a Chinese character (Simplified or Traditional).

    Args:
        char (str): A single character to check.

    Returns:
        bool: True if the character is Chinese, False otherwise.

    Raises:
        ValueError: If the input is not a single character.
    """
    if len(char) != 1:
        raise ValueError("Input must be a single character.")

    ranges = [
        ('\u4e00', '\u9fff'),    # CJK Unified Ideographs
        ('\u3400', '\u4dbf'),    # CJK Unified Ideographs Extension A
        ('\u20000', '\u2a6df'),  # CJK Unified Ideographs Extension B
        ('\u2a700', '\u2b73f'),  # CJK Unified Ideographs Extension C
        ('\u2b740', '\u2b81f'),  # CJK Unified Ideographs Extension D
        ('\u2b820', '\u2ceaf'),  # CJK Unified Ideographs Extension E
        ('\u2ceb0', '\u2ebef'),  # CJK Unified Ideographs Extension F
        ('\uf900', '\ufaff'),    # CJK Compatibility Ideographs
    ]
    return any(start <= char <= end for start, end in ranges)


def introduce_spaces_to_characters(character_list: List[str], pinyin_list: List[str]) -> List[str]:
    """
    Introduces spaces into a list of characters based on the spaces found in the corresponding pinyin list.

    Args:
        character_list (List[str]): A list of characters (e.g., Chinese characters) to be processed.
        pinyin_list (List[str]): A list of pinyin strings that may contain spaces.

    Returns:
        List[str]: A new list of characters with spaces introduced according to the pinyin list.
    """
    result = []
    character_index = 0

    for pinyin in pinyin_list:
        if pinyin == ' ':  # Space in pinyin
            result.append(' ')
            if character_list[character_index] == ' ':
                character_index += 1  # Skip if both are spaces
        else:
            result.append(character_list[character_index])
            character_index += 1

    return result


def split_by_single_and_double_spaces(input_str: str) -> List[str]:
    """
    Splits a string by single spaces and double spaces, preserving both word and sentence boundaries.

    Args:
        input_str (str): The input string with single and double spaces.

    Returns:
        List[str]: A list where words are individual elements and sentences are separated by single spaces.
    """
    parts = input_str.split('  ')  # Split on double spaces
    result = []

    for part in parts:
        words = part.split(' ')
        result.extend(words)
        result.append(' ')

    if result and result[-1] == ' ':
        result.pop()  # Remove the last unnecessary space

    return result


def replace_extra_space(sentence: str) -> str:
    """
    Replaces single spaces between pinyin syllables with no space (concatenates the words),
    and converts double spaces (indicating real pronunciation breaks) into a single space.

    This function splits the sentence using `split_by_single_and_double_spaces`, removes single spaces
    between words, and maintains the separation for sentence boundaries indicated by double spaces.

    Args:
        sentence (str): A string of pinyin, possibly with single and double spaces.

    Returns:
        str: A cleaned string where single spaces are removed, and double spaces are replaced by a single space.
    """
    if not sentence:
        return ''

    # Step 1: Split the sentence using `split_by_single_and_double_spaces`
    parts = split_by_single_and_double_spaces(sentence)

    # Step 2: Rebuild the sentence, removing single spaces between pinyin words and keeping double-space indications
    cleaned_sentence = ''.join(part if part == ' ' else part for part in parts)

    return cleaned_sentence


def process_synonyms(synonym_string: str) -> str:
    """
    Processes a string of synonyms by marking Chinese characters with tone information.

    Args:
        synonym_string (str): The string containing Chinese synonyms separated by <br>.

    Returns:
        str: A processed string with marked Chinese characters for tone.
    """
    synonyms = synonym_string.split('<br>')
    pattern = re.compile(r'([\u4e00-\u9fff]+)\s*\(([\w\s]+)\)\s*-\s*[\w\s]+')
    processed_synonyms = []

    for synonym in synonyms:
        match = pattern.search(synonym)
        if match:
            characters = match.group(1)
            pinyin = match.group(2)
            marked_chars = get_marked_characters(characters, pinyin)
            processed_synonym = synonym.replace(characters, marked_chars)
            processed_synonyms.append(processed_synonym)
        else:
            processed_synonyms.append(synonym)

    return '<br>'.join(processed_synonyms)


if __name__ == '__main__':
    example_characters = '全球定位系统'
    example_pinyin = 'quán qiú dìng wèi xì tǒng'
    marked_result = get_marked_characters(example_characters, example_pinyin)
    print(example_pinyin)
    print(marked_result)

    example_pinyin_with_spaces = 'quán qiú  dìng wèi  xì tǒng'
    cleaned_pinyin = replace_extra_space(example_pinyin_with_spaces)
    print(cleaned_pinyin)
