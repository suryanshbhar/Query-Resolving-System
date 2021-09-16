from flask import Flask, render_template,url_for, request,redirect,send_file

from werkzeug.utils import secure_filename
import os
from os import path
######################################################################################
import nltk
nltk.download('all')
from nltk.corpus import stopwords
from nltk.tag import pos_tag # for proper noun
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tag import DefaultTagger
import os
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

#######################################################################################
from sentence_transformers import SentenceTransformer, models

word_embedding_model = models.Transformer('embeddings', max_seq_length=256)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])


def preprocess(text):
    text = re.sub(r'(?<=[.])(?=[^\s])(?=[^0-9])', r' ', text)
    
    sent_tokens = nltk.sent_tokenize(text)
   
    word_tokens = nltk.word_tokenize(text)
    word_tokens_lower=[word.lower() for word in word_tokens]
    
    stopWords = list(set(stopwords.words("english")))
    word_tokens_refined=[x for x in word_tokens_lower if x not in stopWords]
    
    stem = []
    ps = PorterStemmer()
    for w in word_tokens_refined:
        stem.append(ps.stem(w))
    word_tokens_refined=stem
    
    if word_tokens_refined[-1]=='?':
        word_tokens_refined=word_tokens_refined[:-1]
    
    return text,sent_tokens,word_tokens,word_tokens_lower,word_tokens_refined


def clean_sentence(sentence,stopwords=False):
    
    sentence=sentence.lower().strip()
    sentence=re.sub(r'[^a-z0-9\s]','',sentence)
    
 
        
    return sentence

def get_cleaned_sentences(text,stopwords=False):
    cleaned_sentences=[]
    sent_tokens = nltk.sent_tokenize(text)
    for sentence in sent_tokens:
        cleaned=clean_sentence(sentence,stopwords)
        cleaned_sentences.append(cleaned)
    return cleaned_sentences



def answer_query(text,query):
    q_text,q_sent_tokens,q_word_tokens,q_word_tokens_lower,q_word_tokens_refined=preprocess(query)
    refined_words_match=[]

    text,sent_tokens,word_tokens,word_tokens_lower,word_tokens_refined=preprocess(text)
    key = get_cleaned_sentences(text)

    for sentence in key:
        sum_text,sum_sent_tokens,sum_word_tokens,sum_word_tokens_lower,sum_word_tokens_refined=preprocess(str(sentence))
        score=0
        for word in q_word_tokens_refined:
            if word in sum_word_tokens_refined:
                score+=1
        refined_words_match.append(score)
    
    tagged = nltk.pos_tag(q_word_tokens)

    query_sentence=key[refined_words_match.index(max(refined_words_match))]
    t_text,t_sent_tokens,t_word_tokens,t_word_tokens_lower,t_word_tokens_refined=preprocess(query_sentence)
    tagged = nltk.pos_tag(t_word_tokens)
    index=0
    temp=[]
    ps = PorterStemmer()
    for t in t_word_tokens_lower:
        if ps.stem(t)==q_word_tokens_refined[index]:
            break
        temp.append(t)
    temp=list(nltk.pos_tag(temp))
 
    answer=[]
    for i in range(len(temp)-1,-1,-1):
        if temp[i][1] not in ['NN','NNS','CD','JJ','JJR','JJS']:
            break
        answer.append(temp[i][0])
    
    if answer == []:
        answer= key[refined_words_match.index(max(refined_words_match))]
    else:
        answer=' '.join(answer[-1::-1])
    return answer







app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html")

text1 =""
question1 =""

@app.route("/convert", methods=["GET", "POST"] )

def convert():
    if request.method == "POST":

       text = request.form.get("text")
       question = request.form.get("question")

       ans = answer_query(text,question)  
       cs = get_cleaned_sentences(text)
       qe = model.encode( question,show_progress_bar=False)
       query_emb = model.encode(cs, show_progress_bar=False)
       similarity_dict={}
       for index ,faq_embedding in enumerate(query_emb):
        sim = cosine_similarity([qe],query_emb[index:index+1])[0][0]
        similarity_dict[cs[index]] = sim
        answer_list = sorted(similarity_dict, key=similarity_dict.get,reverse=True)
        scores=[]
        for a in answer_list:
            scores.append(similarity_dict[a])
    
        answer_list=answer_list[0:5]
        scores=scores[0:5]


       global text1
       global question1
       text1 = text
       question1 = question
       return render_template("answerr.html" , ans=ans, text=text , question=question, answer_list=answer_list,scores=scores)
       
    return render_template("convert.html" , text = text1)





@app.route("/about")
def about():
	return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
