# auto_question_TableQA
根据传入的TableQA类型表自动生成TableQA格式的问题

想要自动生成问题请先运行**writeQA3.py**，再运行**joint.py**  
请注意文件路径以及参数设置  
参数示例见[release-link](https://github.com/WILDCHAP/auto_question_TableQA/releases/download/1.0/default.writeQA)

本代码只能对**TableQA类型的表(json)**进行问题生成  
需要把表转换成TableQA格式请参见[json_2_TableQA](https://github.com/WILDCHAP/json_2_TableQA)

需要特别说明的是，本代码会生成如下类型问题：  
*  根据一个字段查询一个字段
*  根据两个字段and操作查询一个字段

TableQA问题格式如下：  
```json
{
     "table_id": "a1b2c3d4", # 相应表格的id
     "question": "世茂茂悦府的套均面积是多少？", # 自然语言问句
     "sql":{ # 相应SQL
        "sel": [7], # SQL选择的列
        "agg": [0], # 选择的列相应的聚合函数, '0'代表无
        "cond_conn_op": 0, # 条件之间的关系
        "conds": [
            [1,2,"世茂茂悦府"] # 条件列, 条件类型, 条件值，col_1 == "世茂茂悦府"
        ]
    }
}
```
