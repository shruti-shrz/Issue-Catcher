import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer as wn, SnowballStemmer
#from sklearn.feature_extraction.text import CountVectorize
from nltk.stem.porter import *
import numpy as np
import re
np.random.seed(400)
import nltk

import pandas as pd
stemmer = SnowballStemmer("english")
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
import nltk.tokenize as nt
custom_stopwords = ['up','inside',"warn","use","ve","error","true","false",'issue','begin','read','named','open','lines','non','approach','conventional','statement','sample']
def lemmatizer(text):
	return WordNetLemmatizer().lemmatize(text,pos='v')

def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
    	token = lemmatizer(token)
    	if token not in gensim.parsing.preprocessing.STOPWORDS and token not in custom_stopwords:
    		result.append(token)
    return result

new_sample = "Mask RCNN tflite detection speed on android too slow. System information Mobile device (e.g. iPhone 8, Pixel 2, Samsung Galaxy) if the issue happens on mobile device: Android mobile TensorFlow installed from (source or binary): Binary TensorFlow version (use command below): 2.4.0 Python version: 3.7 Describe the current behavior We have converted Mask RCNN to TFLite using this link: https://wathek.medium.com/convert-mask-r-cnn-model-to-tflite-with-tensorflow-2-3-57160d3be18d and Tensorflow-2.4.0 We have used byte buffers for the input and output tensors and have the GPU delegate, multithreading enabled. However it is taking around 35 seconds for detection, which is really not feasible in terms of latency. Describe the expected behavior We expected the inference time to be around 3-5 seconds. How can we reduce the time taken for detection? Are there any changes we can make to the model other than those done in the link above? Any help would be appreciated, thank you."
new_sample = re.sub('[^a-zA-Z0-9]', ' ', new_sample)
#new_sample = re.sub('\s+',' ',new_sample)
def entity_extractor(text):
	ss=nt.sent_tokenize(text)
	tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
	pos_sentences = [nltk.pos_tag(sent) for sent in tokenized_sent]
	print(pos_sentences)
def file_content(word):
	with open("technical_keyword.txt","r") as read_obj:
		for line in read_obj:
			if word in line:
				#print("l: ",line)
				var = re.split(r"[^a-zA-Z0-9]", line)
				#print("s: ",var)
				for i in var:
					#print(i, " before ", word)
					i = stemmer.stem(i)
					word = stemmer.stem(word)
					#print(i, " after ", word)
					if i==word:

						return True
	return False

def nlp_LDA(sample):
	processed_sample = []
	processed_sample.append(preprocess(sample))
	dictionary = gensim.corpora.Dictionary(processed_sample)
	# for k, v in dictionary.iteritems():
	# 	print(k,v)
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
	#print(check_set)
	for word in final_words:
		res = file_content(word)
		if res == True:
			final_keys.append(word)
			print("IN  -> ",word)
	
	# s = file_content("process")
	# print(s)
	return final_keys
			
	
	# pos_sentences = [nltk.pos_tag(sent) for sent in final_words]
	# print(pos_sentences[0])


	# for i in range(len(bow_doc_x)):
	#     print("Word {} (\"{}\") appears {} time.".format(bow_doc_x[i][0], 
	#                                                      dictionary[bow_doc_x[i][0]], 
	#                                                      bow_doc_x[i][1]))

def similar_issues_score(input_issue_keywords, issue_keywords):
	sim_count =0
	for i in input_issue_keywords:
		if i in issue_keywords:
			sim_count+=1
	return sim_count








	

