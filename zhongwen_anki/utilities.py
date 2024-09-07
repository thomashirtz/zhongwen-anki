import re
from typing import Optional, List

from pinyin import get as get_pinyin

from zhongwen_anki.constants import tone_to_vowel_list


def add_mark(character: str, tone: str) -> str:
    """
    Wraps a Chinese character with a mark that represents its tone.

    Args:
        character: The Chinese character to be marked.
        tone: The tone class to be added as a mark.

    Returns:
        The character wrapped in an HTML <mark> tag with the tone class.
    """
    if character == ' ':
        return ' '  # Return space as-is
    return f'<mark class="{tone}">{character}</mark>'


def contains(string: str, substring_list: List[str]) -> bool:
    """
    Checks if any of the substrings in the given list exist in the string.

    Args:
        string: The string to search within.
        substring_list: List of substrings to check for.

    Returns:
        True if any substring is found in the string, False otherwise.
    """
    return any(substring in string for substring in substring_list)


def is_chinese_character(char: str) -> bool:
    """
    Determines if a given character is a Chinese character (Simplified or Traditional).

    Args:
        char: A single character to check.

    Returns:
        True if the character is Chinese, False otherwise.

    Raises:
        ValueError: If the input is not a single character.
    """
    if len(char) != 1:
        raise ValueError("Input must be a single character.")

    # Unicode ranges for common Chinese characters
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


def get_marked_characters(characters: str, pinyin: Optional[str] = None) -> str:
    """
    Adds HTML tone marks to Chinese characters based on their associated pinyin tones.

    Args:
        characters: The string of Chinese characters to mark.
        pinyin: Optional string of pinyin corresponding to the Chinese characters.

    Returns:
        A string where Chinese characters are wrapped with tone-specific HTML <mark> tags.
    """
    character_list = list(characters)

    # If no pinyin provided, generate pinyin for each character
    if pinyin is None:
        pinyin_list = [get_pinyin(c) if is_chinese_character(c) else None for c in character_list if c != '']
    else:
        pinyin_list = [p for p in pinyin.split(' ') if p != ' ' and p != '']

    marked_characters = ''

    # Match characters with their corresponding pinyin and apply marks based on tone
    for character, p in zip(character_list, pinyin_list):
        if p is None:
            marked_characters += character
            continue
        for tone, vowel_list in tone_to_vowel_list.items():
            if contains(p, vowel_list):
                character = add_mark(character, tone)
                break
        marked_characters += character

    return marked_characters


def replace_extra_space(sentence: str) -> str:
    """
    Replaces single spaces between pinyin syllables with no space (concatenates the words),
    and converts double spaces (indicating real pronunciation breaks) into a single space.

    Args:
        sentence: A string of pinyin, possibly with single and double spaces.

    Returns:
        A cleaned string where single spaces are removed and double spaces are replaced by a single space.
    """
    if not sentence:
        return ''

    # Replace all double spaces with a unique placeholder (to mark where real spaces should be)
    sentence = sentence.replace('  ', '<<PLACEHOLDER>>')

    # Remove all remaining single spaces
    sentence = sentence.replace(' ', '')

    # Restore the single space where double spaces were originally present
    sentence = sentence.replace('<<PLACEHOLDER>>', ' ')

    return sentence


def process_synonyms(synonym_string: str) -> str:
    """
    Processes a string of synonyms by marking Chinese characters with tone information.

    Args:
        synonym_string: The string containing Chinese synonyms separated by <br>.

    Returns:
        A processed string with marked Chinese characters for tone.
    """
    synonyms = synonym_string.split('<br>')

    # Regex pattern to match characters and pinyin in the synonym string
    pattern = re.compile(r'([\u4e00-\u9fff]+)\s*\(([\w\s]+)\)\s*-\s*[\w\s]+')

    processed_synonyms = []

    # Process each synonym to mark the characters
    for synonym in synonyms:
        match = pattern.search(synonym)
        if match:
            characters = match.group(1)  # Extract the Chinese characters
            pinyin = match.group(2)  # Extract the pinyin
            # Add marked characters based on pinyin
            marked_characters = get_marked_characters(characters, pinyin)
            processed_synonym = synonym.replace(characters, marked_characters)
            processed_synonyms.append(processed_synonym)
        else:
            # If no match is found, keep the synonym as is
            processed_synonyms.append(synonym)

    # Join processed synonyms back into a single string with <br> separators
    return '<br>'.join(processed_synonyms)


if __name__ == '__main__':
    # Example usage of get_marked_characters
    example_characters = '全球定位系统'
    example_pinyin = 'quán qiú dìng wèi xì tǒng'
    marked_result = get_marked_characters(example_characters)
    print(example_pinyin)
    print(marked_result)

    # Example usage of replace_extra_space
    example_pinyin_with_spaces = 'quán qiú  dìng wèi  xì tǒng'
    cleaned_pinyin = replace_extra_space(example_pinyin_with_spaces)
    print(cleaned_pinyin)
