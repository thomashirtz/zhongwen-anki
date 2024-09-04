import os
import pathlib
import argparse
import requests
import pandas as pd
from zhongwen_anki.utilities import get_marked_characters, replace_extra_space, process_synonyms


def script(
        input_path: str,
        output_path: str,
) -> int:
    """
    Args:
        input_path: File path to the `zhongwen` word list.
        output_path: Output file path.

    Returns:
        Integer indicating the exit code of the function.
    """
    columns = [
        'Simplified', 'Traditional', 'Pinyin', 'Meaning', 'SentenceSimplified', 'SentenceMeaning', 'SentencePinyin',
        'Synonyms', 'DictionarySimplified', 'DictionaryPinyin', 'DictionaryMeaning'
    ]
    dataframe = pd.read_csv(
        filepath_or_buffer=input_path,
        sep='\t',
        names=columns,
        index_col=False,
    )

    try:
        os.remove(output_path)
    except FileNotFoundError:
        pass

    for index, row in dataframe.iterrows():
        dictionary = dict(row)
        word = row['Simplified']

        if word == 'Simplified Characters':
            continue

        print(index, word)

        simplified_marked = get_marked_characters(
            characters=row['Simplified'],
            pinyin=row['Pinyin'],
        )

        traditional_marked = get_marked_characters(
            characters=row['Traditional'],
            pinyin=row['Pinyin'],
        )

        sentence_simplified_marked = get_marked_characters(
            characters=row['SentenceSimplified'],
            pinyin=row['SentencePinyin'],
        )

        row['DictionarySimplified'] = row['DictionarySimplified'].replace(' ', '')  # todo understand why I had to do replaced again
        dictionary_marked = get_marked_characters(
            characters=row['DictionarySimplified'],
            pinyin=row['DictionaryPinyin'],
        )

        dictionary.update(
            {
                'Hint': word[0],
                'SimplifiedColored': simplified_marked,
                'TraditionalColored': traditional_marked,
                'SentenceSimplifiedColored': sentence_simplified_marked,
                'SentencePinyin': replace_extra_space(row['SentencePinyin']),
                'SynonymsColored': process_synonyms(row['Synonyms']),
                'DictionarySimplified': row['DictionarySimplified'],
                'DictionarySimplifiedColored': dictionary_marked,
                'DictionaryPinyin': replace_extra_space(row['DictionaryPinyin']),
            }
        )

        # To be sure that the columns are always in the right order.
        columns = [
            'Simplified', 'SimplifiedColored',
            'Traditional', 'TraditionalColored',
            'Pinyin', 'Meaning', 'Hint',
            'SentenceSimplified', 'SentenceSimplifiedColored', 'SentenceMeaning', 'SentencePinyin',
            'Synonyms', 'SynonymsColored',
            'DictionarySimplified', 'DictionarySimplifiedColored', 'DictionaryPinyin', 'DictionaryMeaning',
        ]

        temporary_dataframe = pd.DataFrame([dictionary])[columns]
        is_file_empty = os.path.exists(output_path) and os.stat(output_path).st_size == 0
        temporary_dataframe.to_csv(
            path_or_buf=output_path,
            sep='\t',
            index=False,
            mode='a',
            header=not os.path.exists(output_path) or is_file_empty
        )
    return 0


def main() -> int:
    """Main function. It is responsible for parsing the arguments, then  it
    will call the card generation script.

    Returns:
        Integer indicating the exit code of the function.
    """
    parser = argparse.ArgumentParser(
        description='zhongwen-anki',
        usage='Use "zhongwen-anki --help" or "za --help" for more information',
    )
    parser.add_argument(
        '-i', '--input',
        type=pathlib.Path, required=True, metavar='',
        help='Input file path.',
    )
    parser.add_argument(
        '-o', '--output',
        type=pathlib.Path, required=True, metavar='',
        help='Output file path.',
    )
    args = parser.parse_args()
    return script(
        input_path=str(args.input),
        output_path=str(args.output),
    )


if __name__ == '__main__':
    input_path = r'..\data\input.txt'
    output_path = r'..\data\output_7.csv'

    script(
        input_path=input_path,
        output_path=output_path,
    )
