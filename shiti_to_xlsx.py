import pandas as pd
import json
import re


def to_xlsx_file(path):
	# 文本和实体文件路径
	text_path = "shiti_data/海军装备.json"
	shiti_path = "shiti_data/海军装备标注结果.json"

	with open(text_path, 'r', encoding='utf-8') as f:
		text_list = []
		for line in f.readlines():
			if line.strip().startswith(u'\ufeff'):
				text = line.strip().encode('utf8')[3:].decode('utf8')
				text_list.append(json.loads(text))
			else:
				text_list.append(json.loads(line.strip()))

	with open(shiti_path, 'r', encoding='utf-8') as f1:
		shiti_list = []
		for line in f1.readlines():
			shiti_list.append(json.loads(line.strip()))

	xlsx_list = []
	for i in range(0, 18578):
		# 英文标点转成中文标点
		text = text_list[i]["内容"].replace(".", "。")
		text = text.replace(";", "；")
		sentence_list = text.split("。")
		# print("内容:", text_list[i]["内容"])
		for sentence in sentence_list:
			if sentence:
				# print("句子：", sentence)
				# 总结只在该句中出现的实体，并去重和去相似
				shiti_dic = quchong(sentence, shiti_list[i])
				# print("实体字典：", shiti_dic)
				# 构建配置：地区、港口、机场、基地- 舰艇、飞机、导弹、战车、部队
				xlsx_list += peizhi(sentence, shiti_dic)
				# 构建竞争、合作、冲突：地区-地区
				xlsx_list += jing_he_chong(sentence, shiti_dic)
				# 构建协同、打击：舰艇、飞机、导弹、战车、部队-舰艇、飞机、导弹、战车、部队
				xlsx_list += xie_da(sentence, shiti_dic)
				# 构建装备：部队-舰艇、飞机、导弹、战车；舰艇-飞机、导弹；飞机-导弹；战车-导弹
				# xlsx_list += zhuangbei(sentence, shiti_dic)
				# 构建隶属：人物-部队
				xlsx_list += lishu(sentence, shiti_dic)
				# 构建路线、目标：舰艇、飞机、导弹、战车、部队-地区、港口、机场、基地
				xlsx_list += lu_mu(sentence, shiti_dic)
		print("文本 ", i, "处理完毕！")
	# print("*" * 30)
	# for item in xlsx_list:
	# 	print(item)

	# result_list = [['1', 1, 1], ['2', 2, 2], ['3', 3, 3]]
	columns = ["标号", "可能的关系", "实体1", "实体2", "文本"]
	dt = pd.DataFrame(xlsx_list, columns=columns)
	dt.to_excel(path, index=0)


# 配置关系：为每一句话构造实体1、实体2、文本形式(# 构建配置：地区、港口、机场、基地- 舰艇、飞机、导弹、战车、部队)
def peizhi(sentence, shiti_dic):
	xlsx_list = []
	entity1_type_list = ["地区", "港口", "机场", "基地"]
	entity2_type_list = ["舰艇", "飞机", "导弹", "战车", "部队"]
	for entity1 in entity1_type_list:
		if shiti_dic[entity1]:
			for didian_entity in shiti_dic[entity1]:
				if didian_entity in sentence:
					for entity2 in entity2_type_list:
						if shiti_dic[entity2]:
							for zhuangbei_entity in shiti_dic[entity2]:
								xlsx = []
								if zhuangbei_entity in sentence:
									xlsx.append(shiti_dic["标号"])
									xlsx.append("配置")
									xlsx.append(didian_entity)
									xlsx.append(zhuangbei_entity)
									xlsx.append(sentence)
									xlsx_list.append(xlsx)
	# if xlsx_list:
	# 	for item in xlsx_list:
	# 		print("待抽数据：", item)
	return xlsx_list


# 为每一句话构造实体1、实体2、文本形式(竞争、合作、冲突：地区-地区)
def jing_he_chong(sentence, shiti_dic):
	xlsx_list = []
	entity1_type_list = ["地区"]
	entity2_type_list = ["地区"]
	for entity1 in entity1_type_list:
		if shiti_dic[entity1]:
			for didian_entity in shiti_dic[entity1]:
				if didian_entity in sentence:
					for entity2 in entity2_type_list:
						if shiti_dic[entity2]:
							for zhuangbei_entity in shiti_dic[entity2]:
								xlsx = []
								if zhuangbei_entity in sentence:
									if didian_entity != zhuangbei_entity:
										xlsx.append(shiti_dic["标号"])
										xlsx.append("竞争、合作、冲突")
										xlsx.append(didian_entity)
										xlsx.append(zhuangbei_entity)
										xlsx.append(sentence)
										xlsx_list.append(xlsx)

	# 删除实体1和实体2颠倒的数据
	for item in xlsx_list[::-1]:
		for item1 in xlsx_list[::-1]:
			if item[2] == item1[3] and item[3] == item1[2]:
				if item in xlsx_list:
					xlsx_list.remove(item)

	# if xlsx_list:
	# 	for item in xlsx_list:
	# 		print("待抽数据：", item)
	return xlsx_list


# 为每一句话构造实体1、实体2、文本形式(协同、打击：舰艇、飞机、导弹、战车、部队-舰艇、飞机、导弹、战车、部队)
def xie_da(sentence, shiti_dic):
	xlsx_list = []
	entity1_type_list = ["舰艇", "飞机", "导弹", "战车", "部队"]
	entity2_type_list = ["舰艇", "飞机", "导弹", "战车", "部队"]
	for entity1 in entity1_type_list:
		if shiti_dic[entity1]:
			for didian_entity in shiti_dic[entity1]:
				if didian_entity in sentence:
					for entity2 in entity2_type_list:
						if shiti_dic[entity2]:
							for zhuangbei_entity in shiti_dic[entity2]:
								xlsx = []
								if zhuangbei_entity in sentence:
									if didian_entity != zhuangbei_entity:
										xlsx.append(shiti_dic["标号"])
										xlsx.append("协作、打击、装备")
										xlsx.append(didian_entity)
										xlsx.append(zhuangbei_entity)
										xlsx.append(sentence)
										xlsx_list.append(xlsx)

	# 删除实体1和实体2颠倒的数据
	for item in xlsx_list[::-1]:
		for item1 in xlsx_list[::-1]:
			if item[2] == item1[3] and item[3] == item1[2]:
				if item in xlsx_list:
					xlsx_list.remove(item)
	# if xlsx_list:
	# 	for item in xlsx_list:
	# 		print("待抽数据：", item)
	return xlsx_list


# # 为每一句话构造实体1、实体2、文本形式(装备：部队-舰艇、飞机、导弹、战车；舰艇-飞机、导弹；飞机-导弹；战车-导弹)
# def zhuangbei(sentence, shiti_dic):
# 	xlsx_list = []
# 	entity1_type_list = [["部队"], ["舰艇"], ["飞机"], ["战车"]]
# 	entity2_type_list = [["舰艇", "飞机", "导弹", "战车"], ["飞机", "导弹"], ["导弹"], ["导弹"]]
# 	for i in range(0, len(entity1_type_list)):
# 		for entity1 in entity1_type_list[i]:
# 			if shiti_dic[entity1]:
# 				for didian_entity in shiti_dic[entity1]:
# 					if didian_entity in sentence:
# 						for entity2 in entity2_type_list[i]:
# 							if shiti_dic[entity2]:
# 								for zhuangbei_entity in shiti_dic[entity2]:
# 									xlsx = []
# 									if zhuangbei_entity in sentence:
# 										xlsx.append(shiti_dic["标号"])
# 										xlsx.append(didian_entity)
# 										xlsx.append(zhuangbei_entity)
# 										xlsx.append(sentence)
# 										xlsx_list.append(xlsx)
# 	if xlsx_list:
# 		for item in xlsx_list:
#
# 			("待抽数据：", item)
# 	return xlsx_list


# 为每一句话构造实体1、实体2、文本形式(隶属：人物-部队)
def lishu(sentence, shiti_dic):
	xlsx_list = []
	entity1_type_list = ["人物"]
	entity2_type_list = ["部队"]
	for entity1 in entity1_type_list:
		if shiti_dic[entity1]:
			for didian_entity in shiti_dic[entity1]:
				if didian_entity in sentence:
					for entity2 in entity2_type_list:
						if shiti_dic[entity2]:
							for zhuangbei_entity in shiti_dic[entity2]:
								xlsx = []
								if zhuangbei_entity in sentence:
									xlsx.append(shiti_dic["标号"])
									xlsx.append("隶属")
									xlsx.append(didian_entity)
									xlsx.append(zhuangbei_entity)
									xlsx.append(sentence)
									xlsx_list.append(xlsx)
	# if xlsx_list:
	# 	for item in xlsx_list:
	#
	#
	#
	#
	# 		("待抽数据：", item)
	return xlsx_list


# 为每一句话构造实体1、实体2、文本形式(路线、目标：舰艇、飞机、导弹、战车、部队-地区、港口、机场、基地)
def lu_mu(sentence, shiti_dic):
	xlsx_list = []
	entity1_type_list = ["舰艇", "飞机", "导弹", "战车", "部队"]
	entity2_type_list = ["地区", "港口", "机场", "基地"]
	for entity1 in entity1_type_list:
		if shiti_dic[entity1]:
			for didian_entity in shiti_dic[entity1]:
				if didian_entity in sentence:
					for entity2 in entity2_type_list:
						if shiti_dic[entity2]:
							for zhuangbei_entity in shiti_dic[entity2]:
								xlsx = []
								if zhuangbei_entity in sentence:
									xlsx.append(shiti_dic["标号"])
									xlsx.append("路线、目标")
									xlsx.append(didian_entity)
									xlsx.append(zhuangbei_entity)
									xlsx.append(sentence)
									xlsx_list.append(xlsx)
	# if xlsx_list:
	# 	for item in xlsx_list:
	# 		print("待抽数据：", item)
	return xlsx_list


# 实体列表去重和去相似
def quchong(sentence, shiti_dic):
	quchong_dic = {}
	shiti_type = ["舰艇", "飞机", "导弹", "战车", "地区", "港口", "机场", "基地", "自然地理", "部队", "人物"]
	quchong_dic["标号"] = shiti_dic["标号"]

	for shiti in shiti_type:
		if shiti_dic[shiti]:
			# 去重
			quchong_dic[shiti] = list(set(shiti_dic[shiti]))
			# 去相似
			for entity in quchong_dic[shiti][::-1]:
				if entity not in sentence:
					quchong_dic[shiti].remove(entity)
			for entity1 in quchong_dic[shiti]:
				for entity2 in quchong_dic[shiti]:
					if entity1 in sentence and entity2 in sentence:
						if entity1 != entity2 and entity1 in entity2:
							if entity1 in quchong_dic[shiti]:
								quchong_dic[shiti].remove(entity1)

		else:
			quchong_dic[shiti] = []

	return quchong_dic


if __name__ == '__main__':
	path = "shiti_data/shiti.xlsx"
	to_xlsx_file(path)
