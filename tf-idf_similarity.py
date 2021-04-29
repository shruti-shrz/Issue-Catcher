# THIS CODE NOT USED ANYMORE, EXPERIMENTED TO SEE IF BETTER RESULTS ARE OBTAINED WITH THIS MODEL
# BERT CHOSEN OVER TF-IDF EVENTUALLY 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

base_document = "Deprecation error with php mod_fcgid: stderr: PHP Fatal error:  Unparenthesized a ? b : c ? d : e is not supported. Use either `(a ? b : c) ? d : e` or `a ? b : (c ? d : e)` in public_html/user/plugins/aboutme/aboutme.php on line 71"


# sample corpus
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
1x: Unparenthesized a ? b : c ? d : e is deprecated. Use either (a ? b : c) ? d : e or a ? b : (c ? d : e)']

def process_tfidf_similarity():
    vectorizer = TfidfVectorizer()

    # To make uniformed vectors, both documents need to be combined first.
    documents.insert(0, base_document)
    #print(documents)
    embeddings = vectorizer.fit_transform(documents)
    #print(embeddings)
    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()
    print(cosine_similarities)
    highest_score = 0
    highest_score_index = 0
    for i, score in enumerate(cosine_similarities):
        print(i , score)
        if highest_score < score:
            highest_score = score
            highest_score_index = i
        #print(documents[i], score)


    most_similar_document = documents[highest_score_index]

    print(most_similar_document, "           ", highest_score)

process_tfidf_similarity()