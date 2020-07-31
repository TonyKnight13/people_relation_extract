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

# 示例语句及预处理

# text1 = '中国#鱼雷攻击型核潜艇#1970年12月26日,中国第一艘鱼雷攻击型核潜艇在北方的一个半岛上,神秘地下水了。'
# text1 = '机枪#飞机#一名士兵用机枪把一架美军飞机打了下来!'
# text1 = '以色列#加沙#以色列对加沙地区的进攻造成了超过1200名巴勒斯坦人死亡,约5300人受伤,其中绝大部分都是无辜平民'
# text1 = '美国海军#加利福尼亚号#美国海军一艘最新核潜艇加利福尼亚号于2011年10月29日服役。'
# text1 = '美海军#SSN-23吉米·卡特号#2004年6月5日,美海军建造的海狼级第3艘,也是该级最后一艘SSN-23吉米·卡特号在美国通用动力公司电船分公司的格罗顿船厂下水。'
# text1 = '以色列#巴勒斯坦#巴以都面临严峻挑战,以犹太种族和民主精神为立国原则的以色列不能永远占据着巴勒斯坦领土,也不能吞并巴勒斯坦,建立两个民族国家并和睦相处是解决巴以冲突的惟一可行方法,但和平之路依旧漫长。'
# text1 = '空军部队#美制RB-57D型蒋机#12天后,新华社公布了国防部的嘉奖令,表扬击落窜扰我华北地区上空的美制RB-57D型蒋机的空军部队。'

# 读取测试数据
df = pd.read_excel('junshi_data/test.xlsx')
# print(df)
df1 = pd.DataFrame(df)
# print(df1)
zhengque_num = 0
num = 0

# 记录预测标签和真实标签
y_ture_list = []
y_pre_list = []
# 结果保存
result_list = []
path = 'predict_result/predict.xlsx'
for index, row in df1.iterrows():
	result = []
	num = index + 1
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
	print('原文: %s' % text1)
	print('预测关系: %s' % id_rel_dict[y])
	y_pre_list.append(id_rel_dict[y])
	y_ture_list.append(row['关系'])
	if id_rel_dict[y] == row['关系']:
		zhengque_num += 1
	else:
		print("真实关系：", row['关系'])
		print("*" * 30)
	result.append(row['实体1'])
	result.append(row['实体2'])
	result.append(row['关系'])
	result.append(id_rel_dict[y])
	result.append(row['文本'])
	result_list.append(result)

columns = ["实体1", "实体2", "true_关系", "pre_关系", "文本"]
dt = pd.DataFrame(result_list, columns=columns)
dt.to_excel(path, index=0)

# 混淆矩阵
labels_list = ["竞争", "合作", "协作", "隶属", "路线", "目标", "共指", "配置", "装备", "unknown", "冲突", "打击"]
c_m = confusion_matrix(y_ture_list, y_pre_list, labels=labels_list)
print("混淆矩阵：")
print(c_m)
n = len(c_m)
print("各关系精确率、召回率：")
for i in range(n):
	rowsum, colsum = sum(c_m[i]), sum(c_m[r][i] for r in range(n))
	print(labels_list[i] + "关系")
	if colsum:
		print('precision: %s' % (c_m[i][i] / float(colsum)))
	if rowsum:
		print('recall: %s' % (c_m[i][i] / float(rowsum)))
	if rowsum == 0 and colsum == 0:
		print('precision: %s' % 0, 'recall: %s' % 0)
	print("*" * 20)
print("*" * 20)
print("关系正确数:", zhengque_num)
print("测试总数:", num)
print("准确率：", zhengque_num / num)
