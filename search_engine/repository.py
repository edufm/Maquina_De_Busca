'''Funções para manipulação de corpus, repositórios e indices.
'''
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk.corpus as nltk_corpus
import nltk
import json
import re


# -------------------------- Criação dos jsons --------------------------------
def create_repo(corpus, do_stopwords=True, do_normalize=True):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    # Verifica se o pacote de stopwords ja esta baixado
    
    if do_stopwords:
        nltk.download('stopwords')
        eng_stopwords = stopwords.words("english")
    if do_normalize:
        stemmer = PorterStemmer()
    
    repo = {}
    for docid, text in corpus.items():
        # Remove caracteres especiais (tudo que não é letra ou digito)
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text, flags=re.DOTALL|re.MULTILINE)

        # tokenize
        text_tokens = word_tokenize(text)

        # Remove stop_words
        if do_stopwords:
            text_tokens = [word for word in text_tokens if not word in eng_stopwords]

        # Normalize
        if do_normalize:
            text_tokens = [stemmer.stem(word) for word in text_tokens]

        repo[docid] = text_tokens

    return repo

    

def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''
    indexed = defaultdict(lambda:defaultdict(int))
    
    for doc_id, words in repo.items():
        for word in words:
            indexed[word][doc_id] +=1

    return indexed


def save(data, filename):
    with open(f"{filename}.json", 'w') as file:
        json.dump(data, file, indent=4)

def load(filename):
    with open(f"{filename}.json", 'r') as file:
        return json.load(file)
    