import argparse
from pathlib import Path
from typing import List

import pandas as pd

from new_utilities import (
    sentence_to_words,
    words_to_simplified,
    words_to_pinyin,
    words_to_coloured_html,
    process_synonyms,
)


def _transform_row(row: pd.Series) -> dict:
    """Return a fully processed row ready for output."""
    simplified_words = sentence_to_words(row["Simplified"])
    traditional_words = sentence_to_words(row["Traditional"])
    sentence_words = sentence_to_words(row["SentenceSimplified"])
    dictionary_words = sentence_to_words(row["DictionarySimplified"].replace(" ", ""))

    return {
        # primary fields
        "Simplified": row["Simplified"],
        "SimplifiedColored": words_to_coloured_html(simplified_words),
        "Traditional": row["Traditional"],
        "TraditionalColored": words_to_coloured_html(traditional_words),
        "Pinyin": row["Pinyin"],
        "Meaning": row["Meaning"],
        "Hint": row["Simplified"][0],
        # sentence
        "SentenceSimplified": words_to_simplified(sentence_words),
        "SentenceSimplifiedColored": words_to_coloured_html(sentence_words),
        "SentenceMeaning": row["SentenceMeaning"],
        "SentencePinyin": words_to_pinyin(sentence_words),
        # synonyms
        "Synonyms": row["Synonyms"],
        "SynonymsColored": process_synonyms(row["Synonyms"]),
        # dictionary
        "DictionarySimplified": words_to_simplified(dictionary_words),
        "DictionarySimplifiedColored": words_to_coloured_html(dictionary_words),
        "DictionaryPinyin": words_to_pinyin(dictionary_words),
        "DictionaryMeaning": row["DictionaryMeaning"],
    }

REQUIRED_COLS: List[str] = [
    "Simplified", "Traditional", "Pinyin", "Meaning",
    "SentenceSimplified", "SentenceMeaning", "Synonyms",
    "DictionarySimplified", "DictionaryMeaning",
]

OUTPUT_COLUMNS: List[str] = [
    "Simplified", "SimplifiedColored",
    "Traditional", "TraditionalColored",
    "Pinyin", "Meaning", "Hint",
    "SentenceSimplified", "SentenceSimplifiedColored", "SentenceMeaning", "SentencePinyin",
    "Synonyms", "SynonymsColored",
    "DictionarySimplified", "DictionarySimplifiedColored", "DictionaryPinyin", "DictionaryMeaning",
]


def generate_flashcards(input_path: Path, output_path: Path) -> None:
    """Read *input_path* TSV, enrich it, and write to *output_path*.

    The TSV **must** contain at least the columns listed in `REQUIRED_COLS`.
    Extra columns are silently ignored.
    """
    try:
        df = pd.read_csv(
            input_path,
            sep="\t",
            dtype=str,
            usecols=REQUIRED_COLS,  # enforces presence of all mandatory cols
        )
    except ValueError as exc:
        missing_match = (
            "Usecols do not match" in str(exc) or "Missing column provided"
            in str(exc)
        )
        if missing_match:
            raise SystemExit(
                f"❌ Input file {input_path} is missing one or more required "
                f"columns: {', '.join(REQUIRED_COLS)}"
            ) from exc
        raise

    # fill NaN with empty string to avoid None issues downstream
    df = df.fillna("")

    processed_rows = [_transform_row(row) for _, row in df.iterrows()]
    out_df = pd.DataFrame(processed_rows, columns=OUTPUT_COLUMNS)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_path, sep="\t", index=False, encoding="utf-8")

    print(f"✅ Wrote {len(out_df):,} cards → {output_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="zhongwen‑anki",
        description="Generate Chinese flashcards with tone colouring.",
    )
    parser.add_argument("-i", "--input", type=Path, required=True, metavar="INPUT.tsv",
                        help="Path to Zhongwen word list (TSV).")
    parser.add_argument("-o", "--output", type=Path, required=True, metavar="OUTPUT.tsv",
                        help="Destination TSV for Anki.")
    return parser.parse_args()


def main() -> None:  # noqa: D401 – script entry‑point
    args = _parse_args()
    generate_flashcards(args.input, args.output)


if __name__ == "__main__":
    generate_flashcards(args.input, args.output)
