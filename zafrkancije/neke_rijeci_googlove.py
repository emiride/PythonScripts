from gensim.models.word2vec import Word2Vec
import gensim
import numpy as np


model = gensim.models.KeyedVectors.load_word2vec_format('filtered.bin', binary=True)
most_similar = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=5)
most_similar1 = model.most_similar('baklava', topn=5)
print(most_similar1)
print(most_similar)