## naive bayes
usage: 

+ bayeslearner.py path/to/train.csv path/to/bayes.model
+ bayesclassfier.py bayes.model test.csv result.csv
###.model格式
```
attributes: str
class_index: str
classes: str
values: str
model_data: str
```

## KNN
usage: 

+ knnclassifier.py k train.csv test.csv result.csv

## 其他
util.py 中实现了csv文件的读写
## 环境
已测试：python 3.6, pypy 3.8