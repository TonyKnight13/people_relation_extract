# -*- coding: utf-8 -*-
import json
import pandas as pd
from pprint import pprint


def withdev(train_df,dev_df,test_df):
    with open('train.txt', 'w', encoding='utf-8') as f1:
        for text, rel in zip(train_df['text'].tolist(), train_df['rel'].tolist()):
            f1.write(str(rel)+' '+text+'\n')

    with open('dev.txt', 'w', encoding='utf-8') as f2:
        for text, rel in zip(dev_df['text'].tolist(), dev_df['rel'].tolist()):
            f2.write(str(rel)+' '+text+'\n')

    with open('test.txt', 'w', encoding='utf-8') as f3:
        for text, rel in zip(test_df['text'].tolist(), test_df['rel'].tolist()):
            f3.write(str(rel)+' '+text+'\n')

def withoutdev(train_df,test_df):
    with open('example.train', 'w', encoding='utf-8') as f1:
        for text, rel in zip(train_df['text'].tolist(), train_df['rel'].tolist()):
            f1.write(str(rel)+' '+text+'\n')

    with open('example.test', 'w', encoding='utf-8') as f2:
        for text, rel in zip(test_df['text'].tolist(), test_df['rel'].tolist()):
            f2.write(str(rel)+' '+text+'\n')   

if __name__ == '__main__':
    df = pd.read_excel('law_relation(total).xlsx')
    relations = list(df['可能的关系'].unique())
    relation_dict = {}
    relation_dict.update(dict(zip(relations, range(1, len(relations)+1))))

    with open('rel_dict.json', 'w', encoding='utf-8') as h:
        h.write(json.dumps(relation_dict, ensure_ascii=False, indent=2))
    print('总数: %s' % len(df))
    pprint(df['可能的关系'].value_counts())
    df['rel'] = df['可能的关系'].apply(lambda x: relation_dict[x])
    
    texts = []
    for per1, per2, text in zip(df['实体1'].tolist(), df['实体2'].tolist(), df['文本'].tolist()):
        text = '$'.join([per1, per2, text.replace(per1, len(per1)*'#').replace(per2, len(per2)*'#')])
        texts.append(text)

    df['text'] = texts
    print(df['text'])
    
    train_df = df.sample(frac=0.7, random_state=1024)
    temp_df = df.drop(train_df.index)
    dev_df = temp_df.sample(frac=0.66, random_state=1024)
    test_df = temp_df.drop(dev_df.index)

    withdev(train_df,dev_df,test_df)
    withoutdev(train_df,temp_df)














