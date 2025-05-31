import html
from dataclasses import dataclass
from typing import List, Union

import jieba
from pypinyin import Style, pinyin as _pinyin
from zhongwen_anki.constants import tone_to_vowel_list, vowel_to_tone

@dataclass(slots=True)
class Character: # todo maybe change to syllable
    """One Hanzi plus phonetic information."""

    pinyin: str
    simplified: str # todo remove simplified and change this to character
    traditional: str # todo remove traditional
    tone: int  # 1‒5 (5 = neutral)

    # ——— convenience ———
    def simplified_marked(self) -> str:
        """Return `<mark class="toneN">char</mark>` with N = self.tone."""
        return f'<mark class="tone{self.tone}">{html.escape(self.simplified)}</mark>'


@dataclass(slots=True)
class Word:
    raw: str
    is_chinese: bool
    parts: List[Character | str]

    def __iter__(self):
        return iter(self.parts)

def _is_chinese_character(ch: str) -> bool:
    """Return *True* iff *ch* is in any UCS block that contains Hanzi."""
    ranges = (
        ("\u4E00", "\u9FFF"),   # CJK Unified Ideographs
        ("\u3400", "\u4DBF"),   # Extension A # todo do i need those for chinese ?
        ("\u20000", "\u2A6DF"), # Extension B
        ("\u2A700", "\u2B73F"), # Extension C
        ("\u2B740", "\u2B81F"), # Extension D
        ("\u2B820", "\u2CEAF"), # Extension E
        ("\u2CEB0", "\u2EBEF"), # Extension F
        ("\uF900", "\uFAFF"),   # Compatibility Ideographs
    )
    return any(start <= ch <= end for start, end in ranges)


def _tone_from_tone3(py: str) -> int:
    """Extract the final digit of a TONE3 syllable; neutral → 5."""
    for c in reversed(py):
        if c.isdigit():
            return int(c)
    return 5  # neutral / fifth tone


def sentence_to_words(sentence_text: str) -> List[Word]:
    """Segment *sentence_text* and return a flat `list[Word]`."""
    if not sentence_text or not sentence_text.strip():
        return []

    segment_list = [segment for segment in jieba.lcut(sentence_text) if segment]
    words: List[Word] = []

    for segment in segment_list:
        is_cn = any(_is_chinese_character(c) for c in segment)

        if is_cn:
            marks = _pinyin(segment, style=Style.TONE,  errors="default", heteronym=False)
            nums  = _pinyin(segment, style=Style.TONE3, errors="default", heteronym=False)

            chars: List[Character] = [] # todo rename with list
            for idx, hanzi in enumerate(segment):
                chars.append(
                    Character(
                        pinyin=marks[idx][0],
                        simplified=hanzi,
                        traditional=hanzi,  # swap in OpenCC if needed # todo remove
                        tone=_tone_from_tone3(nums[idx][0]),
                    )
                )
            words.append(Word(raw=segment, is_chinese=True, parts=chars))
        else:
            words.append(Word(raw=segment, is_chinese=False, parts=[segment]))

    return words


def words_to_simplified(words: List[Word]) -> str:
    """Concatenate `word.raw` across the list."""
    return "".join(word.raw for word in words)


def words_to_pinyin(words: List[Word], *, sep: str = " ") -> str:
    """Return a pinyin string with tone marks; non‑Chinese segments stay verbatim."""
    syllables: List[str] = []
    for word in words:
        if word.is_chinese:
            syllables.extend(char.pinyin for char in word.parts)  # type: ignore[arg-type]
        else:
            syllables.append(word.raw)
    return sep.join(syllables)


def words_to_coloured_html(words: List[Word]) -> str:
    """Return the sentence with tone‑coloured `<mark>` tags."""
    buf: List[str] = []
    for word in words:
        if word.is_chinese:
            buf.extend(char.simplified_marked() for char in word.parts)  # type: ignore[arg-type]
        else:
            buf.append(html.escape(word.raw))
    return "".join(buf)

def process_synonyms(synonym_string: str) -> str:
    """Colour‑mark the Hanzi in a `<br>`‑separated synonyms string **without**
    altering any punctuation or existing HTML tags.

    Example input
        "矢量 (shǐ liàng) - vector<br>量向 (liàng xiàng) - vector"

    Returns the same string with Hanzi wrapped in `<mark class="toneN">…</mark>`.
    """
    if not synonym_string:
        return ""

    entries = synonym_string.split("<br>")
    coloured_entries: List[str] = []

    for entry in entries:
        words = sentence_to_words(entry)
        coloured_entries.append(words_to_coloured_html(words, escape_non_chinese=False))

    return "<br>".join(coloured_entries)



def _detect_tone(syllable: str) -> int:
    for ch in syllable:
        if ch in accent_to_tone:
            return accent_to_tone[ch]
    if syllable and syllable[-1].isdigit():
        d = int(syllable[-1])
        if 1 <= d <= 4:
            return d
    return 5  # neutral

# ---------------------------------------------------------------------------
# build Word list from explicit pinyin
# ---------------------------------------------------------------------------

def chars_with_pinyin_to_words(chars: str, pinyin_str: str) -> List[Word]:
    """Return `[Word]` representing *chars* coloured according to *pinyin_str*."""

    pinyin_list = pinyin_str.strip().split()
    parts: List[Character] = []

    for idx, ch in enumerate(chars):
        if _is_chinese_character(ch):
            pinyin = pinyin_list[idx] if idx < len(pinyin_list) else ''
            tone = _detect_tone(pinyin)
            parts.append(Character(pinyin=pinyin, simplified=ch, traditional=ch, tone=tone))
        else:
            # keep punctuation as raw str in the same structure
            parts.append(ch)

    return [Word(raw=chars, is_chinese=True, parts=parts)]

if __name__ == '__main__':

    def debug_word_repr(words):
        repr_lines = []
        for w in words:
            if w.is_chinese:
                chars_info = ",".join(f"{c.simplified}({c.pinyin},{c.tone})" for c in w.parts)  # type: ignore[arg-type]
                repr_lines.append(f"CN[{chars_info}]")
            else:
                repr_lines.append(f"TXT[{w.raw}]")
        return " | ".join(repr_lines)


    examples = [
        "你好世界",
        "你好，世界！",
        "我喜欢Python和C++。",
        "这是一个测试。",
        "银行的行长姓行",
        "你好   世界",
        "  leading and trailing spaces  ",
        "你好，世界！123 numbers"
    ]

    outputs = []

    for sent in examples:
        words = sentence_to_words(sent)
        outputs.append({
            "Sentence": sent,
            "WordList": debug_word_repr(words),
            "Simplified": words_to_simplified(words),
            "Pinyin": words_to_pinyin(words),
            "HTML": words_to_coloured_html(words)
        })

    import pandas as pd

    df = pd.DataFrame(outputs)
    print(df)

