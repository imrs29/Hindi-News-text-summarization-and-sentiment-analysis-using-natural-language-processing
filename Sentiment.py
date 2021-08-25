#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import codecs
from nltk.tokenize import word_tokenize
from sklearn.metrics.classification import accuracy_score
from sklearn.metrics import f1_score


# In[4]:


import warnings
warnings.filterwarnings('ignore')


# In[5]:


data = pd.read_csv("HindiSentiWordnet.txt", delimiter=' ')

fields = ['POS_TAG', 'ID', 'POS', 'NEG', 'LIST_OF_WORDS']
df = data.head()
df


# In[6]:


words_dict = {}
for i in data.index:
     print (data[fields[0]][i], data[fields[1]][i], data[fields[2]][i], data[fields[3]][i], data[fields[4]][i])

     words = data[fields[4]][i].split(',')
     for word in words:
        words_dict[word] = (data[fields[0]][i], data[fields[2]][i], data[fields[3]][i])


# In[7]:


def sentiment(text):
    words = word_tokenize(text)
    votes = []
    pos_polarity = 0
    neg_polarity = 0
    
    allowed_words = ['a','v','r','n']
    for word in words:
        if word in words_dict:
    
            pos_tag, pos, neg = words_dict[word]
            #print(word, pos_tag, pos, neg)
            
            if pos_tag in allowed_words:
                if pos > neg:
                    pos_polarity += pos
                    votes.append(1)
                elif neg > pos:
                    neg_polarity += neg
                    votes.append(0)

    pos_votes = votes.count(1)
    neg_votes = votes.count(0)
    if pos_votes > neg_votes:
        return 1
    elif neg_votes > pos_votes:
        return 0
    else:
        if pos_polarity < neg_polarity:
            return 0
        else:
            return 1
        


# In[12]:


pred_y = []
actual_y = []

pos_reviews = codecs.open("pos_hindi.txt", "r", encoding='utf-8', errors='ignore').read()
for line in pos_reviews.split('$'):
    data = line.strip('\n')
    if data:
        pred_y.append(sentiment(data))
        actual_y.append(1)

print(len(actual_y))
neg_reviews = codecs.open("neg_hindi.txt", "r", encoding='utf-8', errors='ignore').read()
for line in neg_reviews.split('$'):
    data=line.strip('\n')
    if data:
        pred_y.append(sentiment(data))
        actual_y.append(0)
print(len(actual_y))
print("Accuracy=", accuracy_score(actual_y, pred_y) * 100)
print('F-measure: ',f1_score(actual_y,pred_y))


if __name__ == '__main__':
    sentiment1=sentiment(" फिल्म की कास्टिंग जबरदस्त है")
    if sentiment1==1:
        print("Sentiment is positive")
    else:
        print("Sentiment is negative")


# In[ ]:





# In[ ]:




