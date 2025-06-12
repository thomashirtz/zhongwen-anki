import html
from dataclasses import dataclass
from typing import List, Callable
import jieba
from pypinyin import Style, pinyin as _pinyin
from zhongwen_anki.constants import tone_to_vowel_list, vowel_to_tone
from constants import vowel_to_tone
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


def sentence_to_words(
    sentence_text: str,
    *,
    jieba_cut: Callable[[str], List[str]] = jieba.lcut,
) -> List[Word]:
    """
    Segment *sentence_text* into a flat list[Word] while keeping the
    pinyin database *aligned character-for-character* with the original
    string.

    1.  Run **pypinyin on the whole sentence** so the model
        disambiguates polyphonic characters by context.
    2.  Pass `errors=lambda s: list(s)` so *each* non-Hanzi character
        becomes its own one-element group, keeping perfect 1-to-1
        alignment between the returned list and the source string.
    3.  Use the same cursor to walk through both the pinyin list and
        Jieba’s tokens, so every Hanzi ends up with the syllable pypinyin
        has already chosen.
    """
    if not sentence_text or not sentence_text.strip():
        return []

    # --- 1 · pinyin for the whole sentence --------------------------------
    pinyin_marks = _pinyin(
        sentence_text,
        style=Style.TONE,        # marks: hǎo
        heteronym=False,
        errors=lambda bad: list(bad),   # 1 group per char
    )
    pinyin_nums = _pinyin(
        sentence_text,
        style=Style.TONE3,       # numbers: hao3
        heteronym=False,
        errors=lambda bad: list(bad),
    )
    # flatten (one string per original character)
    pinyin_marks = [grp[0] for grp in pinyin_marks]
    pinyin_nums  = [grp[0] for grp in pinyin_nums]

    # --- 2 · Jieba segmentation ------------------------------------------
    tokens = [tok for tok in jieba_cut(sentence_text) if tok]

    words: List[Word] = []
    idx = 0          # cursor into pinyin_* lists

    for tok in tokens:
        if any(_is_chinese_character(c) for c in tok):
            # ---------------- Chinese word ----------------
            parts: List[Character] = []
            for ch in tok:
                py_mark = pinyin_marks[idx]
                py_num  = pinyin_nums[idx]
                parts.append(
                    Character(
                        pinyin=py_mark,
                        simplified=ch,
                        traditional=ch,
                        tone=_tone_from_tone3(py_num),
                    )
                )
                idx += 1
            words.append(Word(raw=tok, is_chinese=True, parts=parts))
        else:
            # ---------------- non-Chinese token ----------------
            words.append(Word(raw=tok, is_chinese=False, parts=[tok]))
            idx += len(tok)   # advance by number of characters

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


def words_to_coloured_html_(words: List[Word]) -> str:
    """Return the sentence with tone‑coloured `<mark>` tags."""
    buf: List[str] = []
    for word in words:
        if word.is_chinese:
            buf.extend(char.simplified_marked() for char in word.parts)  # type: ignore[arg-type]
        else:
            buf.append(html.escape(word.raw))
    return "".join(buf)

def words_to_coloured_html(
    words: List[Word], *, sep: str = "", escape_non_chinese: bool = True
) -> str:
    """Return `sentence_text` where every Hanzi is wrapped in <mark class="toneN">.

    *sep* joins the converted segments – use a single space for sentence &
    dictionary fields, and empty string for headwords.  If *escape_non_chinese*
    is False, non-Chinese substrings are inserted verbatim (useful for the
    synonym field which already contains its own HTML & punctuation).
    """
    rendered: List[str] = []
    for word in words:
        if word.is_chinese:
            rendered.append("".join(char.simplified_marked() for char in word.parts))  # type: ignore[arg-type]
        else:
            rendered.append(html.escape(word.raw) if escape_non_chinese else word.raw)
    return sep.join(rendered)


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
        if ch in vowel_to_tone:
            return vowel_to_tone[ch]
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

