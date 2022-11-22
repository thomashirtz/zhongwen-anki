# chinese-card-generator

This extension is done to create cards using vocabulary saved with the [Zhongwen](https://github.com/cschiller/zhongwen) browser extension.

The base information are taken from zhongwen. Then, additional field are added to the cards using different websites/librairies/apis.

<div align="center">
<table>
<tr>
	<th>Field</th>
	<th>Subfield</th>
	<th>Method</th>

</tr>
<tr>
	<td rowspan='1' colspan='2' >Simplified Characters</td>
	<td rowspan='4' colspan='1' ><a href="https://github.com/cschiller/zhongwen">Zhongwen</a>: Data exported from the browser extension word list.</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Traditional Characters</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Pinyin</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Meaning</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Hint</td>
	<td>Python's slicing method (To keep only the first pinyin letter)</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Sentence Example</td>
	<td rowspan='2' colspan='1' ><a href="https://tatoeba.org/">Tatoeba</a>'s API.</td>
</tr>
<tr>
	<td rowspan='1' colspan='2' >Sentence Meaning</td>
</tr>
<tr>
	<td rowspan='4' colspan='1' >Synonyms</td>
	<td>Characters</td>
	<td rowspan='2' colspan='1' ><a href="https://github.com/chatopera/Synonyms">ChatOpera</a>'s library coupled with the <a href="https://github.com/tsroten/hanzidentifier">hanzidentifier</a> library.</td>
</tr>
<tr>
	<td>Score</td>
</tr>
<tr>
	<td>Pinyin</td>
	<td><a href="https://github.com/lxyu/pinyin">pinyin</a> library</td>
</tr>
<tr>
	<td>Meaning</td>
	<td><a href="https://github.com/nidhaloff/deep-translator">deep-translator</a> library</td>
</tr>
</table>
</div>

## Installation

```console
pip install git+https://github.com/thomashirtz/zhongwen-anki#egg=zhongwen-anki
```

## Utilization

Download your zhongwen word list, then run:

```
zhongwen-anki -i 'input_file_path' -o 'output_file_path'
```

## License

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
