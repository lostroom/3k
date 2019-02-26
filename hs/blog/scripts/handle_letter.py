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

def main(theme, message):

    #Функция убирает лишние символы по границе текста,точки , запятые и проч.
    def mk_trans_tab(chars2remove):
        return str.maketrans(dict(zip(chars2remove, list(' ' * len(chars2remove)))))

    transl_tab = mk_trans_tab(list(string.punctuation) + list('\r\n«»\–'))

    total_text = (theme+' '+message).translate(transl_tab).lower()

    st_w = set(stopwords.words('russian') + [u'мой',u'свой',u'твой',u'который', u'это'])

    words_filtered = []
    i = 0

    morph = pymorphy2.MorphAnalyzer()

    total_text_tok = word_tokenize(total_text)
    for w in total_text_tok:
        if w not in st_w:
            parsed_words = morph.parse(w)[0]
            #print ('parsed_words ', parsed_words)
            normalized_words = parsed_words.normal_form
            #print ('normalized_words ', normalized_words)
            if normalized_words not in st_w:
                words_filtered.append(normalized_words)
                count = FreqDist(words_filtered)
        #print(j['meta_id'])
    return(dict(count))
    #.most_common(20)
    #print (st_w)
    #print (group_df)
    #print (df)
