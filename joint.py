import json
import os


def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        load_dict = json.load(f)
        for i in range(len(load_dict)):
            item=load_dict[i]
            item = json.dumps(item, ensure_ascii=False)
            # 转为tableQA的正常格式
            output_name = os.path.join('result_question', split + '.json')
            with open(output_name, "a", encoding='utf-8') as f2:
                f2.write(item + "\n")
#
# for i in [1,2]:
#     file_name="data1/excel_%s" %i+".json"
#     load_json(file_name)

split = "test" # 运行修改这里
file_name = os.path.join('result_question', split + '_temp.json')      # 你刚刚生成的json问题
load_json(file_name)
