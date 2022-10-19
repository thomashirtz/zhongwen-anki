import pandas as pd


def get_dataframe(file_path: str) -> pd.DataFrame:
    dataframe = pd.read_csv(
        filepath_or_buffer=file_path,
        sep='\t',
        names=['Simplified', 'Traditional', 'Pinyin', 'Meaning', '']
    )
    return dataframe.iloc[:, :-1]  # Zhongwen create files with an extra blank row


if __name__ == '__main__':
    file_path = r'..\data\input.txt'
    dataframe = get_dataframe(file_path=file_path)
    print(dataframe.head())
