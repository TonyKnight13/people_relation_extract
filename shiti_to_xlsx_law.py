import pandas as pd
import json
import re

# tpath:文本路径，epath：实体标注路径，opath：输出表格路径


def derivePL(origin_path):
    peizhi_list = []
    with open(origin_path, 'r', encoding='utf-8') as file:
        text = file.read()
        peizhi = text.split("\n\n")
        for i in range(0, len(peizhi)):
            peizhi_list_temp = peizhi[i].split("\n")
            peizhi_list.append(peizhi_list_temp.pop(0))
    return peizhi_list


def to_xlsx_file(tpath, epath, opath, peizhi_list,e_id_list):
    with open(epath, 'r', encoding='utf-8') as f1:
        people_dict = {}
        text = f1.read()
        people_list = text.split("\n\n")
        for i in range(0, len(people_list)):
            entity_list = people_list[i].split("\n")
            people_dict[peizhi_list[i]] = entity_list

    with open(tpath, 'r', encoding='utf-8') as f2:
        text = f2.read()
        json_str = json.loads(text)
        o_list = []
        for i in json_str:
            index = i["id"]
            text = i["判决书"]
            sen_list = text.split("\n")
            sen_list_new = []
            for sen in sen_list:
                if "。" in sen:
                    sen_listinlist = sen.split("。")
                    if "" in sen_listinlist:
                        sen_listinlist.remove("")
                    for sl in sen_listinlist:
                        sl += "。"
                        sen_list_new.append(sl)
                    else:
                        sen_list_new.append(sen)
            for sen in sen_list_new:
                for eid in e_id_list:
                    
    # for sen in sen_list:

    #     isbianhu(sen)
    #     istonghuo(sen)
    #     iszhengshi(sen)
    #     istongji(sen)
    #     ischongtu(tonglei)
if __name__ == '__main__':
    entity_id_list = [4,5,6,7]
    peizhi_list = derivePL('peizhi.txt')
    to_xlsx_file('新判决书.json', 'people_list.txt', 'r.xlsx', peizhi_list,entity_id_list)
