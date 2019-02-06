import pandas as pd
import json
import numpy as np
import math
def main():

    df = pd.read_csv('blog/media/downloads/org_struct.csv', encoding='utf-8', sep=';', header=None)

    df.columns = ['id','tabnum','name','position', 'boss_id','division']

    data ={}
    data['nodes'] = []
    data['edges'] = []

    for i,j in df.iterrows():
        data['nodes'].append({"label": j['name'], "id": int(j['id']), "shape": 'circularImage', "image": '../../media/photos/man_icon.png'})
        if  j['boss_id'] == j['boss_id']:
            #print (int(j['boss_id']))
            data['edges'].append({"from": int(j['id']), "to": int(j['boss_id']), "id": "e"+str(i)})

    with open('blog/static/jsons/org_struct_graph.json', 'w+') as outfile:
        json.dump(data, outfile)
