'''Funções para manipulação de corpus, repositórios e indices.
'''
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import PorterStemmer
import nltk
import json
import re


# -------------------------- Criação dos jsons --------------------------------
def create_repo(corpus, stopwords=(True, "preset"), normalize=(True, "lower")):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.
        do_stopwords: tupla informando se as stopwords devem ser removidas 
                      e se sim qual metodo deve ser usado: "preset" ou "freq" 
                      ou uma lista das suas próprias palavras
        do_normalize: tupla  informando se a normalização das palavras deve ser feita
                      e se sim qual metodo deve ser usado: "lower" ou "stemmer" 

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    # Verifica qual tipo de stopwords será usado, por frequencia, predefinidas, ou customizadas pelo usuario
    if stopwords[0]:
        if isinstance(stopwords[1], list) or isinstance(stopwords[1], set):
            eng_stopwords = list(stopwords[1])
        
        elif stopwords[1] == "freq":
            first = ""
            words = first.join(corpus.values())
            freq_dist = nltk.FreqDist( word_tokenize(words))
            thresh    = sum(freq_dist.values())         
            eng_stopwords  = list(set(word for word in freq_dist.keys() if (freq_dist[word]/thresh > 0.03 and len(word) > 2)))  

        elif stopwords[1] == "preset":
            nltk.download('stopwords')
            eng_stopwords = nltk_stopwords.words("english")
            
        else:
            raise Exception("stopwords of type {stopwords[1]} not inplemented yet, available types are \
                                                'preset', 'auto' or a custom list")
    
    # Verifica qual tipo de normalização será usado, apenas tirar maisuculas ou um stteming completo
    if normalize[0]:
        if normalize[1] == "lower":
            stem = str.lower
            
        elif normalize[1] == "stemmer":
            stemmer = PorterStemmer()
            stem = stemmer.stem
            
        else:
            raise Exception("normalize of type {normalize[1]} not inplemented yet, available types are \
                                                'stemmer' or 'lower'")
        
    # Com os parametro definidos, itera sobre os Docids
    repo = {}
    for docid, text in corpus.items():
        # Remove caracteres especiais (tudo que não é letra ou digito)
        text = re.sub(r"\n", r"", text, flags=re.DOTALL|re.MULTILINE)
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text, flags=re.DOTALL|re.MULTILINE)

        # tokenize
        text_tokens = word_tokenize(text)

        # Remove stopwords
        if stopwords[0]:
            text_tokens = [word for word in text_tokens if not word in eng_stopwords]

        # Normalize
        if normalize[0]:
            text_tokens = [stem(word) for word in text_tokens]

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


def create_semantic_index(repo):
    '''Indexa as palavras de um corpo para seu tipo semantico

    Args:
        index: um dicionario que mapeia token para lista de docids.

    Returns:
        A relação entre as palavras e seu tipo semantico
    '''    
    # Define as macro classes
    translator = {"AT":"articles", "IN":"preposition", "LS":"marker", "DT":"determinator",
                  "POS":"genitives", "TO":"to", "UH":"interjection",  "CC":"conjunction",
                  "WDT":"wh", "WP":"wh", "WP$":"wh", "WRB":"wh", "EX":"there",
                  "MD":"modal", "PDT":"pre-determiner",  "RP":"particle",
                  "PRP":"pronoun", "PRP$":"pronoun",
                  "FW":"foreing word", 
                  "JJ":"adjective", "JJR":"adjective", "JJS":"adjective",
                  "RB":"adverb", "RBR": "adverb", "RBS": "adverb",
                  "VB":"verb", "VBG":"verb", "VBD":"verb", "VBN":"verb", "VBP":"verb", "VBZ":"verb",
                  "NN":"noun", "NNS":"noun", "NNP":"proper noun", "NNPS":"proper noun",
                  "CD":"number"}
    
    # Define os scores/2 das classes
    points = {"articles":0, "marker":0, "genitives":0, "to":0, "determinator":0,
              "preposition":0.05, "interjection":0.05, "conjunction":0.05, "wh":0.05, "there":0.05,
              "modal":0.2, "pre-determiner":0.1, "particle":0.2, "pronoun":0.1,
              "adjective":0.3, "adverb":0.3, "verb":0.4, "noun":0.4,  
              "proper noun":0.5, "foreing word":0.5, "number":0.5}
    
    index = defaultdict(int)
    for doc_id in repo.keys():
        
        semantic_index = nltk.pos_tag(repo[doc_id])
        
        for key, value in semantic_index:
            index[doc_id] += 2*points[translator[value]]
        
        index[doc_id] = round(index[doc_id]/len(repo[doc_id]), 2)
            
    return index


def save(data, file):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)

def load(file):
    with open(file, 'r') as file:
        return json.load(file)
    