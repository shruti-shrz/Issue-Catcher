import numpy
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
model.max_seq_length = 512

# returns dictionary of similar issues, containing url and score
def getSimilarBert(urls, documents):

    #encoding all documents
    embeddings = model.encode(documents, convert_to_tensor=True)

    #Compute cosine-similarities for each sentence with each other sentence
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    num_cosine = numpy.array(cosine_scores[0])
    sort_index = numpy.argsort(num_cosine)

    ans = []
    for i in range(2, min(7, len(sort_index) +1)):
        d = {
            'url': urls[sort_index[-i]],
            'score': num_cosine[sort_index[-i]]
        }
        ans.append(d)
    return ans

# urls = ['a', 'b', 'c', 'd']
# documents = ['I like chocolate', 'I like eating chocolates', 'I do not like chocolates', 'I love chocolates']

# print(getSimilarBert(urls, documents))