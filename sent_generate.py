#!/usr/bin/env python      
# -*- coding: utf-8 -*-     
# Author: feng

from ciLin import CilinSimilarity
import jieba
import jieba.posseg as pos
from bosonnlp import BosonNLP
nlp = BosonNLP('ChcudxXB.27650.bTlwXAJrIeOD')


sentence = "我想办理信用卡"
sentence = "花呗如何还款"

# sent = list(jieba.cut(sentence))
# sent_pos = list(pos.cut(sentence))
# [pair('我', 'r'), pair('想', 'v'), pair('办理', 'n'), pair('信用卡', 'n')]
# [pair('花', 'v'), pair('呗', 'y'), pair('如何', 'r'), pair('还款', 'v')]

result = nlp.tag(sentence)[0]  # todo  加载新词/热词+词性
sent = result['word']
sent_pos = result['tag']
# {'word': ['我', '想', '办理', '信用卡'], 'tag': ['r', 'v', 'v', 'n']}
# {'word': ['花呗', '如何', '还款'], 'tag': ['n', 'r', 'v']}


# >> result = nlp.tag("紫金直销银行")[0]
# >>> result
# {'word': ['紫金', '直销', '银行'], 'tag': ['nz', 'n', 'n']}
# >>> result = nlp.tag("产品直销广东")[0]
# >>> result
# {'word': ['产品', '直销', '广东'], 'tag': ['n', 'v', 'ns']}


cilinob = CilinSimilarity()  # todo  little bugs
# >>> cilinob.word_code['我']
# ['Aa02', 'Aa02A', 'Aa05A', 'Aa02A01=', 'Aa05A01=', 'Aa02', 'Aa02A', 'Aa05A', 'Aa02A01=', 'Aa05A01=']


# 模板 todo
# 扩充同义词词林 todo


# 规则1：名词前后附近的动词，寻找该动词的近义词
# 动词 - v/vd/vi/vl  名词 - n/nz
# 规则2：todo

nou_dict = {}
for index_, pos_ in enumerate(sent_pos):
    if pos_ == 'n':
        nou_dict[pos_] = index_

verb_dict = {}
verb_dict['v_pre'] = None
verb_dict['v_suf'] = None
if len(sent_pos[:nou_dict['n']]):
    for index_, pos_ in enumerate(sent_pos[:nou_dict['n']]):
        if pos_ == 'v':
            verb_dict[pos_+'_pre'] = index_
    for index_, pos_ in enumerate(sent_pos[nou_dict['n']:]):
        if pos_ == 'v':
            verb_dict[pos_+'_suf'] = index_
            break
else:
    for index_, pos_ in enumerate(sent_pos[nou_dict['n']:]):
        if pos_ == 'v':
            verb_dict[pos_+'_suf'] = index_
            break


from itertools import repeat
def syn_collection(sentlist, topn=5):
    sent_list = []
    for index, word in enumerate(sentlist):
        each = tuple(repeat(word,topn))
        if index in [verb_dict['v_pre'],verb_dict['v_suf']]:
            code_ = cilinob.word_code[word]
            if len(code_):
                code_ = set(code_)
                syncode = [i for i in code_ if i.endswith('=')]
                if len(syncode):
                    listinlist =[cilinob.code_word[i] for i in syncode]
                    synword = tuple(set([l for b in listinlist for l in b]))[:topn]
                    each = synword
            # else:
            #     # 从词向量提取近义词:  todo
        sent_list.append(each)
    return sent_list

sent_list = syn_collection(sent)
print(sent_list)


# word combination - generate syn sentence
from itertools import product
result = list(set(product(*sent_list)))
print(result)

# [('我', '想', '做', '信用卡'), ('我', '想', '办', '信用卡'), ('我', '想', '干', '信用卡'), ('我', '想', '办理', '信用卡'), ('我', '想', '操办', '信用卡')]
# [('花呗', '如何', '还贷'), ('花呗', '如何', '还债'), ('花呗', '如何', '偿付'), ('花呗', '如何', '还款'), ('花呗', '如何', '偿还')]
