import os
import pathlib
import argparse
import requests
import pandas as pd

from zhongwen_anki.utilities import get_marked_characters
from zhongwen_anki.synonyms import SynonymsFinder, EmptySynonymsFinder, BaiduSynonymsFinder  # noqa: W0611
from zhongwen_anki.sentence import SentenceFinder, EmptySentenceFinder, ZaixianSentenceFinder  # noqa: W0611
from zhongwen_anki.meaning import MeaningFinder, EmptyMeaningFinder, CidianMeaningFinder  # noqa: W0611


def script(
        input_path: str,
        output_path: str,
        sentence_finder: SentenceFinder = ZaixianSentenceFinder(),
        meaning_finder: MeaningFinder = CidianMeaningFinder(),
        synonym_finder: SynonymsFinder = BaiduSynonymsFinder(),
) -> int:
    """Script used to transform a `zhongwen` word list to a new file containing
    more information. Example sentences are added using a `SentenceFinder` module
    while the synonyms are found using a `SynonymsFinder` module.

    Args:
        input_path: File path to the `zhongwen` word list.
        output_path: Output file path.
        sentence_finder: A `SentenceFinder` module.
        synonym_finder: A `SynonymsFinder` module.

    Returns:
        Integer indicating the exit code of the function.
    """
    dataframe_input = pd.read_csv(
        filepath_or_buffer=input_path,
        sep='\t',
        names=['Simplified', 'Traditional', 'Pinyin', 'Meaning', '']
    )
    dataframe_input = dataframe_input.iloc[:, :-1]  # Zhongwen creates files with an extra blank row

    try:
        dataframe_output = pd.read_csv(filepath_or_buffer=output_path, sep='\t')

        input_word_set = set(dataframe_input['Simplified'])
        output_word_set = set(dataframe_output['Simplified'])
        word_list = list(input_word_set - output_word_set)

        dataframe = dataframe_input[dataframe_input['Simplified'].isin(word_list)]

    except (FileNotFoundError, pd.errors.EmptyDataError):
        dataframe = dataframe_input

    for index, row in dataframe.iterrows():
        dictionary = dict(row)
        word = row['Simplified']
        print(index, word)

        simplified_colored = get_marked_characters(
            characters=row['Simplified'],
            pinyin=row['Pinyin'],
        )
        traditional_colored = get_marked_characters(
            characters=row['Traditional'],
            pinyin=row['Pinyin'],
        )

        sentence = sentence_finder(word=word)
        synonyms = synonym_finder(word=word)
        meaning = meaning_finder(word=word)

        dictionary.update(
            {
                'Hint': word[0],
                'SimplifiedColored': simplified_colored,
                'TraditionalColored': traditional_colored,
                'SentenceSimplified': sentence.chinese,
                'SentenceSimplifiedColored': sentence.chinese_colored,
                'SentenceMeaning': sentence.english,
                'SentencePinyin': sentence.pinyin,
                'Synonyms': synonyms.summary,
                'SynonymsColored': synonyms.summary_colored,
                'DictionarySimplified': meaning.chinese,
                'DictionarySimplifiedColored': meaning.chinese_colored,
                'DictionaryPinyin': meaning.pinyin,
                'DictionaryMeaning': meaning.english,
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
    input_path = r'..\data\Zhongwen-Words(6).txt'
    output_path = r'..\data\output_6.csv'
    # input_path = r'..\data\input.txt'
    # output_path = r'..\data\output.csv'

    finished = False
    while not finished:
        try:
            script(
                input_path=input_path,
                output_path=output_path,
            )
            finished = True
        except (requests.exceptions.ProxyError, requests.exceptions.SSLError):
            pass
