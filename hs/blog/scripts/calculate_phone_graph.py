import pandas as pd
import json
def main():
    def create_meta_id(x):
        return str(min(int(x[0]), int(x[1])))+'_'+str(max(int(x[0]), int(x[1])))

    df = pd.read_csv('blog/downloads/phone_log.csv', encoding='utf-8', sep=';')
    df['meta_id'] = df[['id_w1','id_w2']].apply(create_meta_id, axis=1)

    all_workers = list(set(df['id_w1'].tolist() + df['id_w2'].tolist()))

    group_df = df.groupby(['meta_id'], as_index=False).agg({'duration' : sum})
    print (group_df.head())

    data ={}
    data['nodes'] = []
    data['edges'] = []

    for i in all_workers:
        data['nodes'].append({"label": "Vasya "+str(i), "id": int(i)})

    for i,j in group_df.iterrows():
        pairs = j['meta_id'].split('_')
        data['edges'].append({"from": int(pairs[0]), "to": int(pairs[1]), "label": "total sec:"+str(j['duration'])})

    with open('blog/static/jsons/data.json', 'w+') as outfile:
        json.dump(data, outfile)

    print (all_workers)
