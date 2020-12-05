import argparse
import json
import os
import random
'''
{"table_id": "com_message", "question": "你知不知道独立董事为袁彬 武兵书 陆桂明的股票共有多少？",
  "sql": {"agg": [4], "cond_conn_op": 0, "sel": [0], "conds": [[4, 2, "袁彬 武兵书 陆桂明"]]}}
'''

# 生成哪张表的问题
#table_id = 'Table_financial_statements'
# "数据id", "股票代码", "报表名称", "时间", "数据项名称", "数据值", "单位"
cond_op_dict = {0: '大于', 1: '小于', 2: '等于', 3: '不为'}
agg_dict = {0: '', 1: '平均', 2: '最大', 3: '最少', 4: '总个数', 5: '总数'}


def op_rand(type):
    '''
    根据列类型选择cond_op,
    仅real做> < !=
    返回cond_op的 中文 数字
    '''
    cond_op = 2  # 对text为 ==
    if type == 'real':
        cond_op = random.randint(0, 3)
    nl_cond_op = cond_op_dict[cond_op]  # 用自然语言表述运算符
    return nl_cond_op, cond_op

def agg_rand(type):
    # 针对select语句的聚合
    agg = 0  # 对text为 ''
    if type == 'real':
        agg = random.randint(0, 5)
    nl_agg = agg_dict[agg]
    return nl_agg, agg


# q1(单条件): 请问"+cond_c+cond_op+cond_v[i]+"的"+sel+"+agg？    （real做> < != agg)
# 24 *20
'''表格dict信息，针对该类问题提的问题数'''
def questions1(load_dict, q_num):
    # 建议q_num=20条
    headers = load_dict['header']
    row = load_dict['rows']
    types = load_dict['types']
    cond_conn_op=0  # where之间连接条件写死
    QA = []
    li = list(range(0, len(headers)))   # 表头下标范围

    # i遍历列名，根据每一列提问
    for i in li:  # 选一w-col找w-val
        cond_c = headers[i]
        # 随机抽取 q_num 个数，表示随机从3451行里选 q_num 行出来，这样4*100共400条问题
        line_rand = random.sample(range(0, len(row) - 1), int(q_num))
        for j in line_rand:     # 找到该条记录，确定w-val
            cond_v = row[j]
            nl_cond_op, cond_op = op_rand(types[i])     # w-op

            sel_id = random.randint(0, len(headers)-1)  # 随机选一列作为s-col
            while sel_id == i:
                sel_id = random.randint(0, len(headers)-1)
            sel = headers[sel_id]
            nl_agg, agg = agg_rand(types[sel_id])

            q_type = random.randint(0, 9)
            if q_type % 3 == 0:
                if cond_op == 2:    # 如果是等于操作
                    question = "请问" + cond_v[i] + "的" + sel + nl_agg + "是？"
                else:
                    question = "请问" + cond_c + nl_cond_op + cond_v[i] + "的" + sel + nl_agg + "是？"  # 智联招聘的公司网址是什么
            elif q_type % 3 == 1:
                question = "我想知道" + cond_c + nl_cond_op + cond_v[i] + "的" + sel + nl_agg
            else:
                if cond_op == 2:    # 如果是等于操作
                    question = cond_v[i] + "的" + nl_agg + sel + "是？"
                else:
                    question = cond_c + nl_cond_op + cond_v[i] + "的" + nl_agg + sel + "是？"
            QA.append([question, agg, sel_id,cond_conn_op, i, cond_op, cond_v[i]])
    return QA


# cond_op(and or)  选取一列中的两个属性作为where值，用and/or连接
# 共12*40个问题
def questions2(load_dict, q_num):
    headers = load_dict['header']
    row = load_dict['rows']
    types = load_dict['types']
    QA = []
    li = list(range(0, len(headers)))
    # i遍历列名，根据每一列（24列） 提问，只对real
    for i in li:  # i==cond_c_id
        cond_c = headers[i]
        # 随机抽取 q_num 个数，表示随机从3451行里选 q_num 行出来
        line_rand = random.sample(range(0, 3450), q_num)        #这里因为不知道怎么随机 循环取两个 用了3450
        for j in line_rand:
            cond_v1 = row[j]
            cond_v2 = row[j+1]
            nl_cond_op1, cond_op1 = op_rand(types[i])
            nl_cond_op2, cond_op2 = op_rand(types[i])
            sel_id = random.randint(0, 25)  # 每一行随机对一列提问
            while sel_id == i:
                sel_id = random.randint(0, 25)
            sel = headers[sel_id]
            nl_agg, agg = agg_rand(types[sel_id])
            cond_conn_op = random.randint(1, 2)
            if cond_conn_op == 1:
                and_or = "且"
            else:
                and_or = "或"
            question = "你知不知道" + cond_c + nl_cond_op1 + repr(cond_v1[i]) \
                           + and_or + nl_cond_op2 + repr(cond_v2[i])\
                           + sel + nl_agg + "是？"  # 智联招聘的公司网址是什么
            QA.append([question, agg, sel_id,cond_conn_op, i, cond_op1, cond_v1[i], i,cond_op2, cond_v2[i]])
    return QA

# cond_op(and or)  两列对一行提问
def questions3(load_dict,q_num):
    headers = load_dict['header']
    row = load_dict['rows']
    types = load_dict['types']
    QA = []
    li = list(range(0, len(headers)-1))
    # i遍历列名，根据某一列的一行提问
    for i in li:  # i==cond_c_id
        cond_c1 = headers[i]


        # headers的下标i+1是为方便，应该修改

        # 随机产生q_num个数，表示随机从3451行里选q_num行出来
        line_rand = random.sample(range(0, len(row) - 1), int(q_num))
        for j in line_rand:
            cond_v = row[j]     # 随机选中的一行
            # 在选中这一行的基础上再随机选择一列
            '''生成另一列下标'''
            i_2 = random.randint(0, len(headers) - 1)
            while i_2 == i:
                i_2 = random.randint(0, len(headers) - 1)
            cond_c2 = headers[i_2]

            nl_cond_op1, cond_op1 = op_rand(types[i])   # 第一个w-op
            nl_cond_op2, cond_op2 = op_rand(types[i_2]) # 第二个w-op

            sel_id = random.randint(0, len(headers) - 1)  # 每一行随机对一列（select）提问
            while sel_id == i or sel_id == i_2:
                sel_id = random.randint(0, len(headers) - 1)

            sel = headers[sel_id]
            nl_agg, agg = agg_rand(types[sel_id])
            # cond_conn_op = random.randint(1, 2)
            cond_conn_op = 1
            if cond_conn_op == 1:
                and_or = "且"
            else:
                and_or = "或"
            question = "你知不知道" + cond_c1 + nl_cond_op1 + cond_v[i] \
                       + and_or \
                       + cond_c2+ nl_cond_op2 + cond_v[i+1] \
                       + "的" + sel + nl_agg + "是？"  # 你知不知道(姓名)(为)(张三)且(性别)为(男)的(出生年月)(一共)是?
            QA.append([question, agg, sel_id,cond_conn_op, i,cond_op1,cond_v[i],i+1,cond_op2,cond_v[i+1]])
    return QA


def write_json(args):
    # 首先读取已有的json文件中的内容
    item_list = []
    # 文件路径
    table_json_path = os.path.join(args.table_dir, args.split + '.tables.json')
    with open(table_json_path, 'r', encoding='utf-8') as f:
        load_dict = json.load(f)
        # 针对A类型问题提的问题数
        QA = questions1(load_dict, args.qa_num)

        for qa in QA:
            # [question, agg, sel_id,cond_conn_op, i,cond_op1,cond_v[i],i+1,cond_op2,cond_v[i+1]]
            agg = qa[1]
            sel = qa[2]
            cond_conn_op = qa[3]
            if cond_conn_op==0:
                conds=[[qa[4], qa[5], qa[6]]]
            else:
                conds = [[qa[4], qa[5], qa[6]], [qa[7], qa[8], qa[9]]]
            item_dict = {"table_id": args.table_id, "question": qa[0],
                         "sql": {'agg': [agg], 'cond_conn_op': cond_conn_op, 'sel': [sel], 'conds': conds}}

            item_list.append(item_dict)  # 将新传入的dict对象追加至list中

        QC = questions3(load_dict, args.qc_num)

        for qa in QC:
            # [question, agg, sel_id,cond_conn_op, i,cond_op1,cond_v[i],i+1,cond_op2,cond_v[i+1]]
            agg = qa[1]
            sel = qa[2]
            cond_conn_op = qa[3]
            if cond_conn_op == 0:
                conds = [[qa[4], qa[5], qa[6]]]
            else:
                conds = [[qa[4], qa[5], qa[6]], [qa[7], qa[8], qa[9]]]
            item_dict = {"table_id": args.table_id, "question": qa[0],
                         "sql": {'agg': [agg], 'cond_conn_op': cond_conn_op, 'sel': [sel], 'conds': conds}}

            item_list.append(item_dict)  # 将新传入的dict对象追加至list中

        f.close()

    # 将追加的内容与原有内容写回（覆盖）原文件
    result_path = os.path.join('result_question', args.split + '_temp.json')
    with open(result_path, 'w', encoding='utf-8') as f2:
        json.dump(item_list, f2, ensure_ascii=False)

'''2020/12/05修改：增加参数设置'''
args = argparse.ArgumentParser()
args.add_argument("--table_dir", required=False, default='原json表', help='表json存放的文件夹位置')
args.add_argument("--split", required=True, default='train', help='train/dev/test')
args.add_argument("--qa_num", required=True, default=0, help='A类问题个数')
args.add_argument("--qb_num", required=True, default=0, help='B类问题个数')
args.add_argument("--qc_num", required=True, default=0, help='C类问题个数')
args.add_argument("--table_id", required=True,help='表id(非表名)')
args = args.parse_args()

write_json(args)
# with open('com_message.json', 'r', encoding='utf-8') as f:
#     load_dict = json.load(f)
#     questions3(load_dict)
