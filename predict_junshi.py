# -*- coding: utf-8 -*-
# 模型预测
import pandas as pd
import json
import numpy as np
from bert.extract_feature import BertVector
from keras.models import load_model
from att import Attention
from sklearn.metrics import confusion_matrix

# 加载模型
model = load_model('junshi_relation.h5', custom_objects={"Attention": Attention})

# 利用BERT提取句子特征大韩神盾
bert_model = BertVector(pooling_strategy="NONE", max_seq_len=80)

# 读取测试数据
df = pd.read_excel('shiti_data/shiti.xlsx', keep_default_na=False)
# print(df)
df1 = pd.DataFrame(df)
# print(df1)

# 保存结果列表
result_list = []
for index, row in df1.iterrows():
	if index <= 56383:
		dic = {}
		if row['实体1'] and row['实体2']:
			text1 = row['实体1'] + '#' + row['实体2'] + '#' + row['文本']

			per1, per2, doc = text1.split('#')
			text = '$'.join([per1, per2, doc.replace(per1, len(per1) * '#').replace(per2, len(per2) * '#')])
			# print(text)

			# 利用BERT提取句子特征
			vec = bert_model.encode([text])["encodes"][0]
			x_train = np.array([vec])

			# 模型预测并输出预测结果
			predicted = model.predict(x_train)
			y = np.argmax(predicted[0])

			with open('junshi_data/rel_dict.json', 'r', encoding='utf-8') as f:
				rel_dict = json.load(f)

			id_rel_dict = {v: k for k, v in rel_dict.items()}
			# print('原文: %s' % text1)
			# print('预测关系: %s' % id_rel_dict[y])
			# print("*" * 30)
			if id_rel_dict[y] in row["可能的关系"]:
				if [row["标号"], row["实体2"], row["实体1"], "配置", row["文本"]] not in result_list:
					if [row["标号"], row["实体2"], row["实体1"], "路线", row["文本"]] not in result_list:
						if [row["标号"], row["实体2"], row["实体1"], "目标", row["文本"]] not in result_list:
							dic["标号"] = row["标号"]
							dic["实体1"] = row["实体1"]
							dic["实体2"] = row["实体2"]
							dic["关系"] = id_rel_dict[y]
							dic["文本"] = row["文本"]
							result_list.append(dic)
		print(row["标号"], "处理完毕！")

with open('predict_result/result.json', 'w', encoding='utf-8') as f:
	for data in result_list:
		f.write(json.dumps(data, ensure_ascii=False) + '\n')
