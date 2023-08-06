## Quick Start

> supported google and deepl



```python
import mytrans

r = mytrans.google('August 22, 2020 The sky became pitch black due to sudden rain and thunder from the afternoon', target_lang='zh-CN')
print(r.res)	# result of list 
print(r.text)	# source result (unprocessed)
print(r.json)	# source result to dict

r = mytrans.deepl('2020年8月22日 午後から急に雨が降ったり雷が鳴ったりして空が真っ暗になった', target_lang='zh')
print(r.res)
```



## Supported Languages

google 和 deepl 的 lang_code有些不同，需自行识别。

The lang_code of google and deepl is a little different, so you need to identify it yourself.



这里列出常用的 lang_code:

Common lang_code are listed here:

> deepl 只支持下列几种，google则更多。
>
> deepl only supports the following, google has more.

- 中文(Chinese): zh (deepl), zh-CN (google)

- 英语(English): en
- 德语(German): de
- 法语(French): fr
- 西班牙语(Spanish): es
- 葡萄牙语(Portuguese): pt
- 意大利语(Italian): it
- 荷兰语(Dutch): nl
- 波兰语(Polish): pl
- 俄语(Russian): ru
- 日语(Japanese): ja

