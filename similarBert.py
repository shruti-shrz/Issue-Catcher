import pandas as pd
import numpy as np
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
import nltk
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# def most_similar(doc_id,similarity_matrix,matrix):
#     print (f'Document: {documents_df.iloc[doc_id]["documents"]}')
#     print ('\n')
#     print (f'Similar Documents using {matrix}:')
#     if matrix=='Cosine Similarity':
#         print(np.argsort(similarity_matrix[doc_id]))
#         similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
#         print(similar_ix)
#     elif matrix=='Euclidean Distance':
#         similar_ix=np.argsort(similarity_matrix[doc_id])
#     for ix in similar_ix:
#         if ix==doc_id:
#             continue
#         print('\n')
#         print (f'Document: {documents_df.iloc[ix]["documents"]}')
#         print (f'{matrix} : {similarity_matrix[doc_id][ix]}')

# Sample corpus
documents = ['Machine learning is the study of computer algorithms that improve automatically through experience.\
Machine learning algorithms build a mathematical model based on sample data, known as training data.\
The discipline of machine learning employs various approaches to teach computers to accomplish tasks \
where no fully satisfactory algorithm is available.',
'Machine learning is closely related to computational statistics, which focuses on making predictions using computers.\
The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning.',
'Machine learning involves computers discovering how they can perform tasks without being explicitly programmed to do so. \
It involves computers learning from data provided so that they carry out certain tasks.',
'Machine learning approaches are traditionally divided into three broad categories, depending on the nature of the "signal"\
or "feedback" available to the learning system: Supervised, Unsupervised and Reinforcement',
'Software engineering is the systematic application of engineering approaches to the development of software.\
Software engineering is a computing discipline.',
'A software engineer creates programs based on logic for the computer to execute. A software engineer has to be more concerned\
about the correctness of the program in all the cases. Meanwhile, a data scientist is comfortable with uncertainty and variability.\
Developing a machine learning application is more iterative and explorative process than software engineering.'
]

urls = ['a', 'b', 'c', 'd', 'e', 'f']

pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_columns', 0)
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

def getSimilarBert(urls, documents):
    documents_df=pd.DataFrame(list(zip(urls, documents)), columns=['urls','documents'])

    # removing special characters and stop words from the text
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
    document_embeddings = sbert_model.encode(documents_df['documents_cleaned'])

    documents_df['sim_score'] = cosine_similarity(document_embeddings)[0]
    print(documents_df.sort_values(by='sim_score', ascending = False))

getSimilarBert(urls, documents)