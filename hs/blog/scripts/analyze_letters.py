import pandas as pd
import json
from ..models import Worker, Letter
import time
import ast

from collections import OrderedDict
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def main():

    c = Letter.objects.order_by('letter_date')
    letter_list = [[i.letter_date, i.letter_theme, i.letter_message, i.letter_dict, i.letter_from, i.letter_to, i.letter_from.tabnum, i.letter_to.tabnum]  for i in c]

    df2 = pd.DataFrame(data=letter_list, columns=['day_of_letter', 'theme', 'message', 'dict', 'from', 'to', 'from_tabnum', 'to_tabnum'])
    df2['day_of_letter'] = pd.to_datetime(df2['day_of_letter'], format='%Y-%m-%d')

    def create_key(x):
        if x[0]>=x[1]:
            return str(x[1])+'_'+str(x[0])
        else:
            return str(x[0])+'_'+str(x[1])
    def dict_from_string(x):
        return ast.literal_eval(x)

    df2['key'] = df2[['from_tabnum', 'to_tabnum']].apply(create_key, axis=1)
    df2['dict'] = df2['dict'].apply(dict_from_string)

    dv = DictVectorizer()
    #D = [{'foo': 1, 'bar': 2}, {'foo': 3, 'baz': 1}]
    D = df2['dict'].tolist()

    X = dv.fit_transform(D)
    tv = TfidfTransformer()
    tfidf = tv.fit_transform(X)

    word2tfidf = dict(zip(dv.get_feature_names(), tv.idf_))
    sorted_by_value = sorted(word2tfidf.items(), key=lambda kv: kv[1])

    print(sorted_by_value)

    '''gdf = df2.groupby(['day_of_call', 'key'], as_index=False).agg({'call_date' : 'count', 'duration' : 'sum'})
    gdf['javatime'] = gdf['day_of_call'].apply(lambda x: int(time.mktime(x.timetuple()))*1000)

    for i, j in gdf.iterrows():
        pass
    print (gdf.head())


    df2 = pd.DataFrame(data=call_list, columns=['day_of_call', 'duration', 'from', 'to'])
    df2['day_of_call'] = pd.to_datetime(df2['day_of_call'], format='%Y-%m-%d')

    df3 = df1.merge(df2, how='left', left_on='day_of_year', right_on='day_of_call')
    gdf = df3.groupby('day_of_year', as_index=False)['duration'].sum()
    gdf['javatime'] = gdf['day_of_year'].apply(lambda x: int(time.mktime(x.timetuple()))*1000)
    test_pack = gdf[['javatime','duration']].values.tolist()

    total_duration = df2['duration'].sum()
    avg_duration = int(df2['duration'].mean())
    day_calls = str(round(df2['duration'].count()/220,2)).replace(',','.')'''

    return
