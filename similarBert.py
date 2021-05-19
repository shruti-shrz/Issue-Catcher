import pandas as pd
import numpy as np
#import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
import nltk
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Sample corpus
'''
documents = ['Deprecation error with php\
mod_fcgid: stderr: PHP Fatal error:  Unparenthesized `a ? b : c ? d : e` is not supported. Use either `(a ? b : c) ? d : e` or `a ? b : (c ? d : e)` in public_html/user/plugins/aboutme/aboutme.php on line 71',
'PHP 7.4 Deprecations/Changes. This issue is meant to track all the deprecation warnings in SuiteCRM when running on PHP 7.4.\
Notable deprecations:\
implode() now emits a deprecation warning when using it with the arguments in reverse order. use implode($glue, $parts) instead of implode($parts, $glue).',
'Deprecation alert from jsm/serializer while using php 7.4.\
When using 2.4.4 (latest 2.x) version of this bundle on php 7.4 environment, you will get this message:\
PHP Deprecated:  Unparenthesized `a ? b : c ? d : e` is deprecated. Use either `(a ? b : c) ? d : e` or `a ? b : (c ? d : e)` in /app/vendor/jms/serializer/src/JMS/Serializer/SerializationContext.php on line 123',
'PHP Unit test show "Unsilenced deprecation notices"\
PHP Unit test:\
1x: Unparenthesized a ? b : c ? d : e is deprecated. Use either (a ? b : c) ? d : e or a ? b : (c ? d : e)'
]
urls = ['a', 'b', 'c', 'd']
'''

pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_columns', 0)
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')


# returns dictionary of similar issues, containing url and score
def getSimilarBert(urls, documents):
    documents_df=pd.DataFrame(list(zip(urls, documents)), columns=['urls','documents'])

    # removing special characters and stop words from the text
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
    document_embeddings = sbert_model.encode(documents_df['documents_cleaned'])

    documents_df['sim_score'] = cosine_similarity(document_embeddings)[0]  # cosine similarity w.r.t input issue
    df = documents_df.sort_values(by='sim_score', ascending = False)  # sorting according to similarity score
    ans = []
    for ind in df.index:
        d = {
            'url': df['urls'][ind],
            'score': df['sim_score'][ind]
        }
        ans.append(d)
    return ans

# getSimilarBert(urls, documents)