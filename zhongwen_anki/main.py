import os
import pathlib
import argparse
import pandas as pd
from zhongwen_anki.utilities import get_marked_characters, replace_extra_space, process_synonyms


def generate_flashcards(input_path: str, output_path: str) -> int:
    """
    Processes a Zhongwen word list and generates an output file in CSV format with enhanced data, including colored characters, synonyms, and dictionary entries.

    Args:
        input_path: Path to the input file containing the Zhongwen word list (tab-separated values).
        output_path: Path where the output CSV file will be saved.

    Returns:
        An integer indicating the exit code. 0 for success.
    """

    # Define the columns in the input file
    columns = [
        'Simplified', 'Traditional', 'Pinyin', 'Meaning', 'SentenceSimplified', 'SentenceMeaning', 'SentencePinyin',
        'Synonyms', 'DictionarySimplified', 'DictionaryPinyin', 'DictionaryMeaning'
    ]

    # Load the input TSV file into a Pandas DataFrame
    dataframe = pd.read_csv(
        filepath_or_buffer=input_path,
        sep='\t',
        names=columns,
        index_col=False,
    )

    # Try to remove the output file if it already exists
    try:
        os.remove(output_path)
    except FileNotFoundError:
        pass  # File doesn't exist, no action needed

    # Iterate through each row of the DataFrame
    for index, row in dataframe.iterrows():
        word_data = dict(row)
        simplified_word = row['Simplified']

        # Skip header row or invalid entries
        if simplified_word == 'Simplified Characters':
            continue

        print(f"Processing index {index}: {simplified_word}")

        # Apply marked characters to relevant fields
        simplified_marked = get_marked_characters(characters=row['Simplified'], pinyin=row['Pinyin'])
        traditional_marked = get_marked_characters(characters=row['Traditional'], pinyin=row['Pinyin'])
        sentence_simplified_marked = get_marked_characters(characters=row['SentenceSimplified'],
                                                           pinyin=row['SentencePinyin'])

        # Remove extra spaces from dictionary simplified characters and re-process
        row['DictionarySimplified'] = row['DictionarySimplified'].replace(' ', '')  # Replaces extra spaces
        dictionary_marked = get_marked_characters(characters=row['DictionarySimplified'],
                                                  pinyin=row['DictionaryPinyin'])

        # Update dictionary with additional processed fields
        word_data.update({
            'Hint': simplified_word[0],  # Use the first character as a hint
            'SimplifiedColored': simplified_marked,
            'TraditionalColored': traditional_marked,
            'SentenceSimplifiedColored': sentence_simplified_marked,
            'SentencePinyin': replace_extra_space(row['SentencePinyin']),
            'SynonymsColored': process_synonyms(row['Synonyms']),
            'DictionarySimplified': row['DictionarySimplified'],
            'DictionarySimplifiedColored': dictionary_marked,
            'DictionaryPinyin': replace_extra_space(row['DictionaryPinyin']),
        })

        # Ensure that columns are written in a specific order
        output_columns = [
            'Simplified', 'SimplifiedColored',
            'Traditional', 'TraditionalColored',
            'Pinyin', 'Meaning', 'Hint',
            'SentenceSimplified', 'SentenceSimplifiedColored', 'SentenceMeaning', 'SentencePinyin',
            'Synonyms', 'SynonymsColored',
            'DictionarySimplified', 'DictionarySimplifiedColored', 'DictionaryPinyin', 'DictionaryMeaning',
        ]

        # Create a temporary DataFrame with the updated row
        temporary_dataframe = pd.DataFrame([word_data])[output_columns]

        # Check if output file is empty or does not exist
        is_file_empty = os.path.exists(output_path) and os.stat(output_path).st_size == 0

        # Append the row to the output file in CSV format (without overwriting existing content)
        temporary_dataframe.to_csv(
            path_or_buf=output_path,
            sep='\t',
            index=False,
            mode='a',
            header=not os.path.exists(output_path) or is_file_empty
        )

    return 0


def main() -> int:
    """
    Main function to handle argument parsing and initiate the flashcard generation process.

    Returns:
        Integer exit code, where 0 indicates successful completion.
    """
    parser = argparse.ArgumentParser(
        description='zhongwen-anki: A tool for generating Chinese flashcards with additional metadata.',
        usage='Use "zhongwen-anki --help" or "za --help" for more information',
    )

    # Define the arguments for input and output file paths
    parser.add_argument(
        '-i', '--input',
        type=pathlib.Path, required=True, metavar='',
        help='Input file path for the Zhongwen word list.',
    )
    parser.add_argument(
        '-o', '--output',
        type=pathlib.Path, required=True, metavar='',
        help='Output file path for the generated flashcards.',
    )

    args = parser.parse_args()

    # Call the script to process the input and generate the output
    return generate_flashcards(
        input_path=str(args.input),
        output_path=str(args.output),
    )


if __name__ == '__main__':
    # Example usage with hardcoded input and output file paths
    input_file = r'../data/input.tsv'
    output_file = r'../data/output.tsv'

    # Call the generate_flashcards function
    generate_flashcards(
        input_path=input_file,
        output_path=output_file,
    )
