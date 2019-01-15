import pandas as pd
import json
def main():
    def create_meta_id(x):
        return str(min(int(x[0]), int(x[1])))+'_'+str(max(int(x[0]), int(x[1])))

    df = pd.read_csv('blog/downloads/phone_log.csv', encoding='utf-8', sep=';', header=None)
    df.columns = ['id_w1','id_w2','duration']
    df['meta_id'] = df[['id_w1','id_w2']].apply(create_meta_id, axis=1)

    all_workers = list(set(df['id_w1'].tolist() + df['id_w2'].tolist()))

    group_df = df.groupby(['meta_id'], as_index=False).agg({'duration' : sum})

    temp_df = df[['id_w2', 'duration']]
    temp_df.columns = ['id_w1', 'duration']
    df_unic = df[['id_w1', 'duration']].append(temp_df)
    df_unic = df_unic.groupby(['id_w1']).agg({'duration' : sum})
    df_unic['rank'] = df_unic['duration'].rank()
    print (df_unic.head())

    df_org = pd.read_csv('blog/downloads/org_struct.csv', encoding='utf-8', sep=';', header=None)
    df_org.columns = ['id','name','position', 'boss_id']
    df_org = df_org.merge(df_unic, how='left', left_on='id', right_on='id_w1')

    data ={}
    data['nodes'] = []
    data['edges'] = []

    for i, j in df_org.iterrows():
        if j['duration'] == j['duration']:
            d = j['duration']/30
            c = "rgba("+str(30*int(j['rank']))+",100,100,1)"
        else:
            d = 5
            c = "rgba(1,100,100,1)"
        data['nodes'].append({"label": j['name'], "id": int(j['id']), "size" : int(d), "color" : c, "data": "olodata"})

    for i,j in group_df.iterrows():
        pairs = j['meta_id'].split('_')
        data['edges'].append({"from": int(pairs[0]), "to": int(pairs[1]), "label": "total sec:"+str(j['duration'])})

    with open('blog/static/jsons/phone_graph.json', 'w+') as outfile:
        json.dump(data, outfile)
