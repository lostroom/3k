import pandas as pd
import json
import numpy as np
import math
def main():

    df = pd.read_csv('blog/downloads/org_struct.csv', encoding='utf-8', sep=';', header=None)

    df.columns = ['id','name','position', 'boss_id']

    data ={}
    data['nodes'] = []
    data['edges'] = []

    for i,j in df.iterrows():
        data['nodes'].append({"label": j['name'], "id": int(j['id'])})
        if  j['boss_id'] == j['boss_id']:
            print (int(j['boss_id']))
            data['edges'].append({"from": int(j['id']), "to": int(j['boss_id']), "label": j['position'], "id": "e"+str(i)})

    with open('blog/static/jsons/org_struct_graph.json', 'w+') as outfile:
        json.dump(data, outfile)
