**Prompt:**

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

Given the list of words:

- 向量 (vector)
- 矩阵 (matrix)
- ...

### Example Output Format (Table)

```
Simplified Characters	Traditional Characters	Pinyin	Meaning	Sentence Example	Sentence Meaning	Pinyin for Sentence	Synonym	DictionarySimplified	DictionaryPinyin	DictionaryMeaning
向量	向量	xiàng liàng	vector	我们需要计算这个向量的长度。	We need to calculate the length of this vector.	wǒ men  xū yào  jì suàn  zhè ge  xiàng liàng  de  cháng dù.	矢量 (shǐ liàng) - vector<br>量向 (liàng xiàng) - vector	数学中用于表示方向和大小的对象	shù xué zhōng  yòng yú  biǎo shì  fāng xiàng  hé  dà xiǎo  de  duì xiàng	object used in mathematics to represent direction and magnitude
矩阵	矩陣	jǔ zhèn	matrix	这个矩阵的行列式为零。	The determinant of this matrix is zero.	zhè ge  jǔ zhèn  de  háng liè shì  wèi líng.	方阵 (fāng zhèn) - square matrix	由数或变量排列成的矩形阵列	yóu shù  huò  biàn liàng  pái liè chéng  de  jù xíng  zhèn liè	rectangle array formed by numbers or variables
```

### Tips for Generating the Table:

1. **Ensure Pinyin Formatting**: Check that there is **one space** between syllables and **two spaces** between separate words in pinyin.
2. **Short but Descriptive Definitions**: The `DictionarySimplified`, `DictionaryPinyin`, and `DictionaryMeaning` columns should provide a concise but informative definition of the term.
3. **Use Simple Example Sentences**: The example sentences should clearly demonstrate the usage of the word in context.
4. **Multiple Synonyms**: Include up to three synonyms, formatted with `<br>` tags to ensure clarity.
5. **Accuracy**: Make sure traditional and simplified characters are accurately paired, and translations and meanings reflect the specific terms.
