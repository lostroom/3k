import pandas as pd
import json
from ..models import Worker, Call
import time
def main():
    c = Call.objects.order_by('call_date')
    call_list = [[i.call_date, i.call_duration, i.call_from, i.call_to, i.call_from.tabnum, i.call_to.tabnum]  for i in c]

    df2 = pd.DataFrame(data=call_list, columns=['day_of_call', 'duration', 'from', 'to', 'from_tabnum', 'to_tabnum'])
    df2['day_of_call'] = pd.to_datetime(df2['day_of_call'], format='%Y-%m-%d')

    def create_key(x):
        if x[0]>=x[1]:
            return str(x[1])+'_'+str(x[0])
        else:
            return str(x[0])+'_'+str(x[1])

    df2['key'] = df2[['from_tabnum', 'to_tabnum']].apply(create_key, axis=1)

    gdf = df2.groupby(['day_of_call', 'key'], as_index=False).agg({'call_date' : 'count', 'duration' : 'sum'})
    gdf['javatime'] = gdf['day_of_call'].apply(lambda x: int(time.mktime(x.timetuple()))*1000)

    for i, j in gdf.iterrows():
        pass
    print (gdf.head())


    '''df2 = pd.DataFrame(data=call_list, columns=['day_of_call', 'duration', 'from', 'to'])
    df2['day_of_call'] = pd.to_datetime(df2['day_of_call'], format='%Y-%m-%d')

    df3 = df1.merge(df2, how='left', left_on='day_of_year', right_on='day_of_call')
    gdf = df3.groupby('day_of_year', as_index=False)['duration'].sum()
    gdf['javatime'] = gdf['day_of_year'].apply(lambda x: int(time.mktime(x.timetuple()))*1000)
    test_pack = gdf[['javatime','duration']].values.tolist()

    total_duration = df2['duration'].sum()
    avg_duration = int(df2['duration'].mean())
    day_calls = str(round(df2['duration'].count()/220,2)).replace(',','.')'''

    return
