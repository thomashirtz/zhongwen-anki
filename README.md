# chinese-card-generator

This extension is done to create cards using vocabulary saved with the [Zhongwen](https://github.com/cschiller/zhongwen) browser extension.

The base information are taken from zhongwen. Then example sentences are added by querying the Totoaba API, the pinyin of the sentence is generated using the [pinyin](https://github.com/lxyu/pinyin) library. Moreover synonyms are added to the entry if avalaible. The synonyms are querried using [chatopera](https://github.com/chatopera/Synonyms) and their meaning are generated using the GoogleTranslate module from the [deep-translator](https://github.com/nidhaloff/deep-translator) library. 
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
