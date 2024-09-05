# Chinese Card Generator

The **Chinese Card Generator** is a Python package designed to streamline the process of creating **Anki flashcards** for learning Chinese. It combines **ChatGPT**-generated content with customized Python processing to turn lists of Chinese words into formatted Anki cards, making it easier to review and learn new Chinese vocabulary.

This package automates the process of:
1. Taking a list of Chinese words and requesting **ChatGPT** to generate related content such as example sentences, synonyms, and dictionary definitions.
2. Processing the generated content using Python scripts to format the data into Anki flashcards.
3. Adding useful tone markings on Chinese characters and providing fields such as **pinyin**, **translations**, **example sentences**, and **synonyms** to facilitate efficient language learning.


## Workflow

1. **Prepare the List of Words**:
   Start by preparing a list of Chinese words in a text file format. This list will be used in a LLM query. e.g:

   ```plaintext
   向量 vector
   矩阵 matrix
   ...
   ```

2. **LLM Query**:
   Use the following prompt to generate the necessary content for each word in the list using ChatGPT or any other LLM:

   ~~~plaintext
   ### Prompt:
   
   Please create a tab-separated table for the given list of Chinese words. Each entry should include the following columns:
   
      1. **Simplified Characters**: The simplified version of the Chinese characters.
      2. **Traditional Characters**: The traditional version of the Chinese characters.
      3. **Pinyin**: The pinyin transcription of the Chinese word, with **one space** between each syllable and **two spaces** between different words (e.g., 'quán qiú  dìng wèi  xì tǒng' for '全球定位系统').
      4. **Meaning**: The English meaning or translation of the word.
      5. **Sentence Example**: A simple example sentence using the word in Chinese.
      6. **Sentence Meaning**: The English translation of the example sentence.
      7. **Pinyin for Sentence**: The pinyin transcription of the example sentence, with **one space** between each syllable and **two spaces** between different words.
      8. **Synonym**: Up to three synonyms for the word, formatted as "SimplifiedCharacters (Pinyin) - Translation", separated by `<br>`.
      9. **DictionarySimplified**: A short definition of the word in Chinese characters, giving a brief explanation of the term's meaning.
      10. **DictionaryPinyin**: The pinyin transcription of the definition, with **one space** between each syllable and **two spaces** between different words.
      11. **DictionaryMeaning**: The English translation of the definition, giving a brief explanation of the term's meaning.
   
   Use the above structure to create the table for each entry from the provided list of words.
   
   ---
   
   ### Example Input
   
      - 向量 (vector)
      - 矩阵 (matrix)
      - ...
   
   ---
   
   ### Example Output
   
   ```
   Simplified Characters	Traditional Characters	Pinyin	Meaning	Sentence Example	Sentence Meaning	Pinyin for Sentence	Synonym	DictionarySimplified	DictionaryPinyin	DictionaryMeaning
   向量	向量	xiàng liàng	vector	我们需要计算这个向量的长度。	We need to calculate the length of this vector.	wǒ men  xū yào  jì suàn  zhè ge  xiàng liàng  de  cháng dù.	矢量 (shǐ liàng) - vector<br>量向 (liàng xiàng) - vector	数学中用于表示方向和大小的对象	shù xué zhōng  yòng yú  biǎo shì  fāng xiàng  hé  dà xiǎo  de  duì xiàng	object used in mathematics to represent direction and magnitude
   矩阵	矩陣	jǔ zhèn	matrix	这个矩阵的行列式为零。	The determinant of this matrix is zero.	zhè ge  jǔ zhèn  de  háng liè shì  wèi líng.	方阵 (fāng zhèn) - square matrix	由数或变量排列成的矩形阵列	yóu shù  huò  biàn liàng  pái liè chéng  de  jù xíng  zhèn liè	rectangle array formed by numbers or variables
   ```
   
   ---
      
   ### Tips for Generating the Table:
   
      1. **Ensure Pinyin Formatting**: Check that there is **one space** between syllables and **two spaces** between separate words in pinyin.
      2. **Short but Descriptive Definitions**: The `DictionarySimplified`, `DictionaryPinyin`, and `DictionaryMeaning` columns should provide a concise but informative definition of the term.
      3. **Use Simple Example Sentences**: The example sentences should clearly demonstrate the usage of the word in context.
      4. **Multiple Synonyms**: Include up to three synonyms, formatted with `<br>` tags to ensure clarity.
      5. **Accuracy**: Make sure traditional and simplified characters are accurately paired, and translations and meanings reflect the specific terms.
   
   ### Word List

   <<WORD LIST HERE>>
   ~~~

   This will generate a table containing all the necessary fields required for the flashcards.


3. **Data Processing**:
   After receiving the generated data from ChatGPT, save the data in a file and use the `zhongwen-anki` package to process the data.
   ```bash
   zhongwen-anki -i 'input_file_path' -o 'output_file_path'
   ```

   The input file path refers to the file with the word list or the table data, and the output file path will contain the processed Anki-ready data.


4. Import the generated output CSV into Anki, and you are ready to start reviewing your new Chinese flashcards!


## Data Fields for Review

When you create your Anki cards using this package, the following fields will be included on each card for effective review:

1. **Simplified Characters**: The modern simplified version of the Chinese word.
2. **Traditional Characters**: The classical traditional form of the word.
3. **Pinyin**: The pronunciation guide with correct tone markings.
4. **Meaning**: The English translation of the word.
5. **Example Sentence**: A simple sentence that demonstrates how the word is used in context, with pinyin and translation.
6. **Synonyms**: Up to three related words or expressions with pinyin and English translations.
7. **Dictionary Entry**:
   - **DictionarySimplified**: A short definition of the word in Chinese.
   - **DictionaryPinyin**: Pinyin transcription of the Chinese definition.
   - **DictionaryMeaning**: The English translation of the definition.
8. **Hint**: The first character of the word to help with recall during reviews.


## Installation

Install the package from the repository:

```bash
pip install git+https://github.com/thomashirtz/zhongwen-anki#egg=zhongwen-anki
```

## License

```
Copyright 2021 Thomas Hirtz

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```