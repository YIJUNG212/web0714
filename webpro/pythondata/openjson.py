import json
dictObj={'哈囉':80,'a':25,'c':60}
fn='out1_8.json'
with open(fn,'w',encoding='UTF-8') as fnObj:
    json.dump(dictObj,fnObj,ensure_ascii=False)