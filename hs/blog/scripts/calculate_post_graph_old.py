import pandas as pd
import json
import numpy as np
import math
import nltk
from nltk.corpus import state_union
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import string
import pymorphy2

def main():
    def create_meta_id(x):
        return str(min(int(x[0]), int(x[1])))+'_'+str(max(int(x[0]), int(x[1])))

    df = pd.read_csv('blog/downloads/post_log.csv', encoding='utf-8', sep=';', header=None)

    df.columns = ['id_w1','id_w2','msg']
    df['meta_id'] = df[['id_w1','id_w2']].apply(create_meta_id, axis=1)

    all_workers = list(set(df['id_w1'].tolist() + df['id_w2'].tolist()))

    group_df = df.groupby('meta_id', as_index = False).agg({'msg' : lambda x: "{%s}" % ', '.join(x)})

    #Функция убирает лишние символы по границе текста,точки , запятые и проч.
    def mk_trans_tab(chars2remove):
        return str.maketrans(dict(zip(chars2remove, list(' ' * len(chars2remove)))))

    transl_tab = mk_trans_tab(list(string.punctuation) + list('\r\n«»\–'))
    group_df['msg'] = group_df['msg'].str.translate(transl_tab).str.lower()

    st_w = set(stopwords.words('russian') + [u'мой',u'свой',u'твой',u'который', u'это'])

    words_filtered = []
    i = 0

    morph = pymorphy2.MorphAnalyzer()

    for i, j  in group_df.iterrows():
        df_tok = word_tokenize(j['msg'])

        for w in df_tok:
            if w not in st_w:
                parsed_words = morph.parse(w)[0]
                #print ('parsed_words ', parsed_words)
                normalized_words = parsed_words.normal_form
                #print ('normalized_words ', normalized_words)
                if normalized_words not in st_w:
                    words_filtered.append(normalized_words)
                    count = FreqDist(words_filtered)
        #print(j['meta_id'])
        print(count.most_common(20))

    #print (st_w)
    #print (group_df)
    #print (df)
