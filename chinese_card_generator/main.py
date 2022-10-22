import pinyin
import pandas as pd
import os

from chinese_card_generator import utilities
from chinese_card_generator import tatoeba
from chinese_card_generator import chatopera


# 1 read the input file
# 2 read the output file
# 3 find the row to do
# 4 append one row at the time to the file


def process_file(
        input_path: str,
        output_path: str,
        num_synonyms: int = 3,
        threshold_synonyms: float = 0.8
):
    dataframe_input = utilities.get_dataframe(input_path)

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
        dictionary['Hint'] = word[0]

        sentence = tatoeba.get_sentence(word=word) # Create SentenceFinder.__call__(word)
        dictionary.update(
            {
                'SentenceSimplified': sentence.chinese,
                'SentenceMeaning': sentence.english,
                'SentencePinyin': pinyin.get(sentence.chinese),
            }
        )

        synonym_list = chatopera.get_synonym_list(
            word=word,
            n=num_synonyms,
            threshold=threshold_synonyms,
        )
        dictionary.update(
            {
                'Synonyms': chatopera.format_synonym_list(synonym_list)  # Create SynonymFinder.__call__(word) + add method for formating
            }
        )

        # To be sure that the columns are in the right order.
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
    output_path = r'..\data\output___.csv'
    process_file(
        input_path=input_path,
        output_path=output_path,

    )
