# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:42:39 2020

@author: test
"""
from bs4 import BeautifulSoup
import csv
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import re
import os

def parse(foldernames,filename):
    #create output file
    fw=open(filename,'w',encoding = 'utf-8')
    writer = csv.writer(fw, lineterminator = '\n')
    
    
    
    #outer loop, go through different folder
    for jobtitle in foldernames:
        path = jobtitle +'/'
        num = 0;
        print(path)
        #inner loop, find all html files
        for i in os.listdir(path):
            print(i)
            text = ''
            pt = path + i
            try:
                #if open,continue
                html = open(pt,encoding = 'utf-8')
            except:
                #if no such file, throw finish and quit
                result =str(num)+jobtitle+' jobs successfully added!'
                print(result)
                break
            num += 1
            
            #parse it
            soup = BeautifulSoup(html,'lxml')
            
            chunk = soup.find('div',{'class':re.compile('jobsearch-jobDescriptionText')})
            lines = chunk.text
            for line in lines:
                text += line
            if jobtitle == 'Data Engineer':
                text = re.sub('data eng[a-z]+',' ',text.lower()).strip()
            if jobtitle == 'Data Scientist':
                text = re.sub('data sci[a-z]+',' ',text.lower()).strip()
            if jobtitle == 'Software Engineer':
                text = re.sub('software eng[a-z]+',' ',text.lower()).strip()
                
            #text = re.sub(jobtitle.lower(),' ',text.lower()).strip()
            writer.writerow([text,jobtitle])
            html.close()
            cur = 'job' + str(num)
            print(cur)

    fw.close()







#find title and jd, store in two arrays

#remove the job category name in the jd








if __name__ == "__main__":
    foldernames = ['Data Engineer','Data Scientist','Software Engineer']
    filename = 'jobposts.txt'
    
    parse(foldernames,filename)
    
