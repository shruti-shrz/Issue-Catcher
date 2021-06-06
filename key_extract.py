#Extract the top relevant keywords for any issue
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import re
np.random.seed(400)
import nltk

#import pandas as pd
stemmer = SnowballStemmer("english")
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# import nltk.tokenize as nt
custom_stopwords = ['up','inside',"warn","use","ve","error","true","false",'issue','begin','read','named','open','lines','non','approach','conventional','statement','sample']
def lemmatizer(text):
	return WordNetLemmatizer().lemmatize(text,pos='v')

def preprocess(text): # cleaning of the issue
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
    	token = lemmatizer(token)
    	if token not in gensim.parsing.preprocessing.STOPWORDS and token not in custom_stopwords:
    		result.append(token)
    return result

#new_sample = re.sub('\s+',' ',new_sample)
def file_content(word): # comapring words with the technical keywords list and returning true if word is technical else false
	with open("technical_keyword.txt","r") as read_obj:
		for line in read_obj:
			if word in line:
				var = re.split(r"[^a-zA-Z0-9]", line)
				for i in var:
					i = stemmer.stem(i)
					word = stemmer.stem(word)
					if i==word:

						return True
	return False

def nlp_LDA(sample): # Extract releveant keywords after preprocessing the sample
	processed_sample = []
	processed_sample.append(preprocess(sample))
	dictionary = gensim.corpora.Dictionary(processed_sample)
	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_sample]
	document_num = 20
	bow_doc_x = bow_corpus[0]
	lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 2, 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 1)
	final_words = []
	final_keys = []
	check_set =set()
	for idx, topic in lda_model.show_topics(-1,10):
		var = topic.split("+")
		print("Topic: {} \nWords: {}".format(idx, topic))
		for word in var:
			word = word.split("*")[1].strip()[1:-1]
			if word not in check_set:
				final_words.append(word)
				check_set.add(word)
	for word in final_words: # the final set of technical keywords after comparing with the technical keywords list
		res = file_content(word)
		if res == True:
			final_keys.append(word)
			print("IN  -> ",word)
	return final_keys

def similar_issues_score(input_issue_keywords, issue_keywords): # giving score to the issue based on the common keywords
	sim_count =0
	for i in input_issue_keywords:
		if i in issue_keywords:
			sim_count+=1
	return sim_count








	

