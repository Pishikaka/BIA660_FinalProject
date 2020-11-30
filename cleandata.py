#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:29:00 2020

@author: yunwang
"""
#import nltk


import pandas as pd
data = pd.read_csv('jobposts.txt', header = None)

data.columns = ['text', 'job title']
data.head()

import re
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

def clean_email_text(text):
    text = text.replace('\n'," ") 
    text = re.sub(r"-", " ", text) 
    text = re.sub(r"\d+/\d+/\d+", "", text) 
    text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", "", text) 
    text = re.sub(r"[\w]+@[\.\w]+", "", text)
    text = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", text) 
    text = re.sub(r'data engineer', '', text)
    text = re.sub(r'data scientist', '', text)
    text = re.sub(r'software engineer', '', text)
    pure_text = ''
    for letter in text:
        if letter.isalpha() or letter==' ':
            pure_text += letter
    text = ' '.join(word for word in pure_text.split() if len(word)>1)
    return text

s_text=data["text"]
data['text'] = s_text.apply(lambda s: clean_email_text(s))
#data.drop(["text"], axis=1)

data.to_csv('data_cleaned.txt', sep='\t', index=False)
#data= data.append('Text':s_text_clean, 'Title':job title), ignore_index= True)
#data.to_csv('dataclean.csv', index= False)
