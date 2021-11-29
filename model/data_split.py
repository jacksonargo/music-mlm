import random
from sklearn.model_selection import train_test_split


with open('data/corpus.txt', encoding='utf-8') as fp:
    sentences = fp.read().split('\n')


random.seed(42069)
random.shuffle(sentences)

benchmark_sentences = sentences[0 : len(sentences)//5]
train_sentences, eval_sentences = train_test_split(sentences[len(sentences)//5:])
