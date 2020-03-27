'''Funções para manipulação de corpus, repositórios e indices.
'''
import json
from collections import defaultdict

import re

import nltk

import nltk.corpus as nltk_corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# -------------------------- Criação dos jsons --------------------------------
def create_corpus(target="reuters"):
    '''Cria o corpus a partir do NLTK

    Args:
        target: Corpo alvo do NLTK
        filename: nome do arquivo de saida para o corpus
    
    Returns:
        Um dicionario que tem os dados do corpus
    '''
    if target == "reuters":
        corpus = nltk_corpus.reuters
    else:
        raise Exception(f"Corpus {target} not implemented yet")

    docs = {}
    for fileid in corpus.fileids():
        docs[fileid] = corpus.raw(fileid)

    return docs


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

# ------------------------ Salvamento dos jsons -------------------------------
def save_corpus(corpus, filename="../storage/Corpus_Reuters"):
    '''Grava um corpus.

    O corpus será gravado como um arquivo JSON.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
        documento completo.
    '''
    with open(f"{filename}.json", 'w') as file:
        json.dump(corpus, file, indent=4)
        

def save_repo(repo, filename="../storage/Repo_Reuters"):
    '''Grava um repositório.

    O repositório será gravado como um arquivo JSON.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.
        filename: nome do arquivo.
    '''
    with open(f"{filename}.json", 'w') as file_repo:
        json.dump(repo, file_repo, indent=4)


def save_index(index, filename="../storage/Index_Reuters"):
    '''Grava um indice reverso.

    O indice será gravado como um arquivo JSON.

    Args:
        index: dicionario que mapeia palavra para um dicionario que mapeia 
        docids para a contagem dessa palavra no documento.
        filename: nome do arquivo.
    '''
    with open(f"{filename}.json", 'w') as file_index:
        json.dump(index, file_index, indent=4)
        
# ----------------------- Carregamento dos jsons ------------------------------
def load_corpus(filename="../storage/Corpus_Reuters"):
    '''Carrega o corpus.

    O corpus deve estar armazenado em formato JSON. Deve ser um dicionário
    mapeando uma string representando o docid de um documento para outra string
    contendo o texto do documento.

    Args:
        filename: nome do arquivo do corpus.

    Returns:
        Um dicionário que mapeia docid (str) para um documento (str).
    '''
    with open(f"{filename}.json", 'r') as file_corpus:
        return json.load(file_corpus)
    
    
def load_repo(filename="../storage/Repo_Reuters"):
    '''Carrega o repo.

    O repo deve estar armazenado em formato JSON. Deve ser um dicionário
    mapeando uma string representando o docid de um documento para outra string
    contendo o texto do documento tokenizado.

    Args:
        filename: nome do arquivo do repo.

    Returns:
        Um dicionário que mapeia docid (str) para um documento tokenizado (str).
    '''
    with open(f"{filename}.json", 'r') as file_repo:
        return json.load(file_repo)
    
    
def load_index(filename="../storage/Index_Reuters"):
    '''Carrega o indice.

    O indice deve estar armazenado em formato JSON. Deve ser um dicionário
    mapeando uma palvra para outro dicionario contendo os DocIds dos documentos
    apeados para o numero de ocorrencias daquela palavra

    Args:
        filename: nome do arquivo do indice.

    Returns:
        Um dicionário que mapeia docid (str) para um dicionario com a contagem 
        de repetições dessa plavra no documeto.
    '''
    with open(f"{filename}.json", 'r') as file_index:
        return json.load(file_index)
