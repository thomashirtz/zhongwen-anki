import html
from dataclasses import dataclass
from typing import List, Union

import jieba
from pypinyin import Style, pinyin as _pinyin

# ---------------------------------------------------------------------------
# Tone helpers
# ---------------------------------------------------------------------------

tone_to_vowel_list: dict[int, List[str]] = {
    1: ['ā', 'ē', 'ī', 'ō', 'ū', 'ǖ', 'Ā', 'Ē', 'Ī', 'Ō', 'Ū', 'Ǖ'],
    2: ['á', 'é', 'í', 'ó', 'ú', 'ǘ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ǘ'],
    3: ['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ', 'Ǎ', 'Ě', 'Ǐ', 'Ǒ', 'Ǔ', 'Ǚ'],
    4: ['à', 'è', 'ì', 'ò', 'ù', 'ǜ', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Ǜ'],
    5: ['a',  'e',  'i',  'o',  'u',  'ü',  'A',  'E',  'I',  'O',  'U',  'Ü'],
}

# reverse lookup → given a vowel with tone mark return its tone number
vowel_to_tone: dict[str, int] = {
    accented: tone for tone, vowel_list in tone_to_vowel_list.items() for accented in vowel_list
}

# ---------------------------------------------------------------------------
# Core dataclasses representing the internal structure of a segmented sentence
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class Character:
    """One Hanzi plus phonetic information."""

    pinyin: str
    hanzi: str  # single character
    tone: int   # 1-5 where 5 = neutral

    # HTML representation with tone-coloured <mark> wrapper
    def marked(self) -> str:
        return f'<mark class="tone{self.tone}">{html.escape(self.hanzi)}</mark>'


@dataclass(slots=True)
class Word:
    """A segment from `jieba` – either Chinese or something else (punctuation, latin)."""

    raw: str
    is_chinese: bool
    parts: List[Union[Character, str]]  # str for non-Chinese glyph inside a Chinese word (rare)

    def __iter__(self):
        return iter(self.parts)

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _is_hanzi(ch: str) -> bool:
    """Return True iff *ch* is a CJK unified ideograph (incl. extensions)."""
    ranges = (
        ("\u4E00", "\u9FFF"),   # Basic
        ("\u3400", "\u4DBF"),   # Ext A
        ("\u20000", "\u2A6DF"), # Ext B
        ("\u2A700", "\u2B73F"), # Ext C
        ("\u2B740", "\u2B81F"), # Ext D
        ("\u2B820", "\u2CEAF"), # Ext E
        ("\u2CEB0", "\u2EBEF"), # Ext F
        ("\uF900", "\uFAFF"),   # Compatibility
    )
    return any(start <= ch <= end for start, end in ranges)


def _tone_from_tone3(py: str) -> int:
    """Extract the trailing digit from a TONE3 pinyin syllable (neutral → 5)."""
    digit = next((int(c) for c in reversed(py) if c.isdigit()), None)
    return digit if digit and 1 <= digit <= 4 else 5

# ---------------------------------------------------------------------------
# Public API – text ↔ structured representation
# ---------------------------------------------------------------------------

def sentence_to_words(sentence_text: str) -> List[Word]:
    """Segment *sentence_text* and produce a flat List[Word].

    Latin words and punctuation are preserved verbatim; Chinese segments are
    further decomposed into Character objects carrying tone and pinyin.
    """
    if not sentence_text or not sentence_text.strip():
        return []

    # `jieba.lcut` conveniently keeps latin substrings intact but removes spaces.
    # We therefore first split by spaces to keep user-provided spacing intact.
    segments: List[str] = []
    for token in sentence_text.split(" "):
        # Re-insert the space that was the delimiter so we can round-trip later
        if segments:
            segments.append(" ")
        segments.extend([seg for seg in jieba.lcut(token) if seg])

    words: List[Word] = []

    for segment in segments:
        if segment == " ":  # preserve explicit space
            words.append(Word(raw=" ", is_chinese=False, parts=[" "]))
            continue

        is_cn = any(_is_hanzi(c) for c in segment)

        if is_cn:
            marks = _pinyin(segment, style=Style.TONE,  errors="default", heteronym=False)
            tone3 = _pinyin(segment, style=Style.TONE3, errors="default", heteronym=False)

            chars: List[Character] = []
            for idx, hanzi in enumerate(segment):
                chars.append(Character(
                    pinyin=marks[idx][0],
                    hanzi=hanzi,
                    tone=_tone_from_tone3(tone3[idx][0]),
                ))
            words.append(Word(raw=segment, is_chinese=True, parts=chars))
        else:
            words.append(Word(raw=segment, is_chinese=False, parts=[segment]))

    return words


# ---------------------------------------------------------------------------
# Formatting helpers (→ various output styles)
# ---------------------------------------------------------------------------

def words_to_simplified(words: List[Word], *, sep: str = "") -> str:
    """Concatenate `word.raw` – default directly, option to keep spaces via *sep*."""
    return sep.join(word.raw for word in words)


def words_to_pinyin(words: List[Word], *, sep: str = " ") -> str:
    """Return a pinyin string, default *single space* separated."""
    syllables: List[str] = []
    for word in words:
        if word.is_chinese:
            syllables.extend(char.pinyin for char in word.parts)  # type: ignore[arg-type]
        else:
            syllables.append(word.raw)
    # Collapse consecutive spaces resulting from preserved literal spaces
    pinyin_str = sep.join(filter(None, syllables))
    return " ".join(pinyin_str.split())  # normalise whitespace


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
            rendered.append("".join(char.marked() for char in word.parts))  # type: ignore[arg-type]
        else:
            rendered.append(html.escape(word.raw) if escape_non_chinese else word.raw)
    return sep.join(rendered)

# ---------------------------------------------------------------------------
# Synonym post-processor
# ---------------------------------------------------------------------------

def process_synonyms(synonym_string: str) -> str:
    """Colour-mark Hanzi in the synonym column while *preserving* existing HTML."""
    if not synonym_string:
        return ""

    coloured_entries: List[str] = []
    for entry in synonym_string.split("<br>"):
        coloured = words_to_coloured_html(
            sentence_to_words(entry), sep="", escape_non_chinese=False
        )
        coloured_entries.append(coloured)
    return "<br>".join(coloured_entries)

# ---------------------------------------------------------------------------
# Helpers for explicit (char, pinyin) lists (used in testing / linting)
# ---------------------------------------------------------------------------

def _detect_tone(syllable: str) -> int:
    # First, try vowel accent
    for ch in syllable:
        if ch in vowel_to_tone:
            return vowel_to_tone[ch]
    # Fallback: trailing digit, else neutral
    if syllable and syllable[-1].isdigit():
        d = int(syllable[-1])
        if 1 <= d <= 4:
            return d
    return 5


def chars_with_pinyin_to_words(chars: str, pinyin_str: str) -> List[Word]:
    """Utility used mainly in tests: build coloured Word list from *chars* + pinyin."""
    pinyin_list = pinyin_str.strip().split()
    parts: List[Character] = []
    for idx, ch in enumerate(chars):
        if _is_hanzi(ch):
            pinyin = pinyin_list[idx] if idx < len(pinyin_list) else ''
            tone = _detect_tone(pinyin)
            parts.append(Character(pinyin=pinyin, hanzi=ch, tone=tone))
        else:
            parts.append(ch)  # keep punctuation as raw str
    return [Word(raw=chars, is_chinese=True, parts=parts)]

# ---------------------------------------------------------------------------
# Quick CLI smoke-test (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    examples = [
        "我们 需要 计算 这个 向量 的 长度 。",
        "请 在 变量 名 中 使用 下划线 。",
    ]
    for sent in examples:
        words = sentence_to_words(sent)
        print("Sentence:", sent)
        print("Simplified:", words_to_simplified(words, sep=" "))
        print("Pinyin:", words_to_pinyin(words))
        print("HTML:", words_to_coloured_html(words, sep=" "))
        print("-" * 60)
