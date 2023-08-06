# 判決書格式轉換
## 使用方法
安裝套件
`
    pip install VerdictFormat
`

把正式格式轉成測試格式
```python
from VerdictFormat import Formal_to_Test
Formal_to_Test(Formal_format_path,output_path)
```

把測試格式轉成正式格式
```python
from VerdictFormat import Test_to_Formal
Test_to_Formal(Test_format_path,output_path)
```

把標記好的格式轉成測試格式
```python
from VerdictFormat import Labeled_to_Test
Labeled_to_Test(Labeled_data)
```

正規化多個法條
```python
from VerdictFormat import Multilaws_to_Normalize
Multilaws_to_Normalize(CJ_text,Match_laws_list,Multilaws_dict_list)
CJ_text : 判決書全文
Match_laws_list : 執掌法條清單
Multilaws_dict_list : 要正規化的法條
```

Formal Format
```python
[
{
    "name": "姓名",
    "statuses": [
        {
          "status":"公務員", 
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        }
      ], 
    "positions": [
        {
          "work unit": "勞動部職業安全衛生署南部職業安全衛生中心",
          "title": "檢查員",
          "locations": 
          [
            {
              "field":"JFull",
              "start": 28, 
              "end":40
            }
          ]
        },
        {
          "work unit": "勞動部職業安全衛生署",
          "title": "職員",
          "locations": []
        }
      ],
    "laws": [
        {
          "act": "貪污治罪條例",
          "article": 4, 
          "paragraph":  1,
          "subparagraph": 2, 
          "locations": 
          [
            {
              "field":"JLaw",
              "start": 28, 
              "end":40
            }, 
            {
              "field":"JLaw",
              "start": 156, 
              "end":168
            }
          ]
        } 
      ]  
  }
]

  ```

Test Format
```python
[
{
		"content_id" : "1" ,
		"name" : "柯森" ,
		"job_location" : [] ,
		"job_title" : [] ,
		"laws" : ["中華民國刑法第276條第1項","中華民國刑法第140條"]
    },{
		"content_id" : "2" ,
		"name" : "吳柯森" ,
		"job_location" : ["停車場"] ,
		"job_title" : ["管理員"] ,
		"laws" : ["中華民國刑法第276條第1項","中華民國刑法第140條"]
    }
]
```

Multilaws Normalize
```python

Multilaws_dict_list=[
        {"start": 2933, "content": "毒品危害防制條例第11條"},
        {"start": 2946, "content": "第13條"},
        {"start": 2951, "content": "第15\r\n條"},
        {"start": 3315, "content": "貪污治罪條例第11條"},
        {"start": 3326, "content": "第133333條第8項\r\n第6款"},
    ]
Normalized_laws_list=['毒品危害防制條例第11條', '毒品危害防制條例第13條', '毒品危害防制條例第15條', '貪污治罪條例第11條', '貪污治罪條例第133333條第8項第6款']

```