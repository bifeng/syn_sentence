# syn_sentence - 同义句生成

+ 同义词来源  
1). 同义词/近义词词林  
2). 语料  
a. 贝叶斯网络/LDA等方法，寻找近义词  
b. word2vec等方法训练词向量，查找同义词  
3). Google翻译/Bing翻译  
输入中文词语，输出英文词语近义词的中文翻译  
注意：垂直领域，需要维护专业的词林。

+ 同义词审核  
构建两个句子，一个是原句，另一个是句子中关键词的同义词列表。  
利用标注工具[1]进行审核并纠正错误的同义词。

+ 同义句编写  
1). synonym of keyword combination  
在垂直领域中，关键词的同义词组合生成同义句的方法足够用了
2). paraphrase generation  
本质上也是解码的过程  


> refer:  
> [1] https://github.com/chakki-works/doccano

