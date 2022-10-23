import os
import pandas as pd

from zhongwen_anki.sentence import SentenceFinder, EmptySentenceFinder, TatoebaSentenceFinder
from zhongwen_anki.synonym import SynonymsFinder, EmptySynonymsFinder, ChatOperaSynonymsFinder


def process_file(
        input_path: str,
        output_path: str,
        sentence_finder: SentenceFinder = TatoebaSentenceFinder(),
        synonym_finder: SynonymsFinder = ChatOperaSynonymsFinder(),
):
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

    except FileNotFoundError:
        dataframe = dataframe_input

    for index, row in dataframe.iterrows():
        dictionary = dict(row)
        word = row['Simplified']

        sentence = sentence_finder(word=word)
        formatted_synonyms = synonym_finder(word=word)
        dictionary.update(
            {
                'Hint': word[0],
                'SentenceSimplified': sentence.chinese,
                'SentenceMeaning': sentence.english,
                'SentencePinyin': sentence.pinyin,
                'Synonyms': formatted_synonyms,
            }
        )

        # To be sure that the columns are always in the right order.
        columns = [
            'Simplified', 'Traditional', 'Pinyin', 'Meaning', 'Hint',
            'SentenceSimplified', 'SentenceMeaning', 'SentencePinyin',
            'Synonyms'
        ]
        temporary_dataframe = pd.DataFrame([dictionary])[columns]
        temporary_dataframe.to_csv(
            path_or_buf=output_path,
            sep='\t',
            index=False,
            mode='a',
            header=not os.path.exists(output_path)
        )


if __name__ == '__main__':
    input_path = r'..\data\Zhongwen-Words.txt'
    output_path = r'..\data\output____.csv'
    process_file(
        input_path=input_path,
        output_path=output_path,

    )
