'''Funções para realzação dos diferentes tipos de busca
'''
import re
import math
from search_engine import corretor
from nltk.tokenize import sexpr_tokenize
from nltk import pos_tag as tagger
from collections import defaultdict

def strip_parenthesis(query):
    
    if query[0] == "(":
        query = query[1:]
    if query[-1] == ")":
        query = query[:-1]
    
    return query.lower().strip(" ")


def busca_docids(index, query, use_corretor=True, in_sub_query=False):
    '''Executa uma query que exige o texto conter as palavras da query com 
       logica "E" (sem parenteses) ou "OR" (entre parenteses).

        Args:
            index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
            repo: dicionario que mapeia docid para uma lista de tokens.
            query: string com as plavras que o documento deve conter
        
        Returns:
            Uma lista com os documentos selecionados.
    '''        
    # Verifia em que nivel de subquery está
    if in_sub_query:
        and_search = False
        or_search=True
    else:
        and_search = True
        or_search=False
    
    # Avança no nivel de subquery
    if "(" in query:
        sub_queries = [strip_parenthesis(q) for q in sexpr_tokenize(query)]
        results = []
        for sub_query in sub_queries:
            _, sub_docids = busca_docids(index, sub_query, in_sub_query=not(in_sub_query))
            results.append(sub_docids)
            
        if or_search:
            docids = set.union(*results)
        elif and_search:
            docids = set.intersection(*results)
    
    # Realiza a busca
    else:
        if use_corretor:
            split_query = [corretor.run(word, list(index.keys())) for word in query.split(" ")]
            query = " "
            query = query.join(split_query).strip(" ")
        
        docids = naive_search(index, query, and_search=and_search, or_search=or_search)
    
    # Mapeia a query para as correções que ocorreram
    if use_corretor:
       query_correct =  {word:corretor.run(word, list(index.keys())) for word in 
                         query.replace("(", "").replace(")","").split(" ")}
       new_query = query
       for word in query_correct.keys():
           new_query = new_query.replace(word, query_correct[word])
       query = new_query
       
    return query, docids


def naive_search(index, query, and_search=False, or_search=False):
    '''Executa uma query que exige o texto conter todas as palavras.

    Args:
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        query: string com as plavras que o documento deve conter
        
    Returns:
        Uma lista com os documentos selecionados.
    '''
    # Parsing da query.
    query = re.sub(r"[^a-zA-Z0-9 ]", "", query, flags=re.DOTALL|re.MULTILINE)
    split_query = query.split(" ")

    # Recuperar os ids de documento que contem todos os termos da query.
    available_words = index.keys()
    score = []
    for word in split_query:
        # Verifica se a palavra esta no corpus
        if word in available_words:
            score.append(set(index[word].keys()))
        else:
            score.append(set())
    # Retornar os textos destes documentos.
    if or_search:
        results = set.union(*score)
    if and_search:
        results = set.intersection(*score)
    
    return results


def rank(docids, index, repo):
    '''Utiliza o TF-IDF para verificar quais documentos tem mais palavras incomuns

    Args:
        docids: lista de documentos para avaliar
        repo: Um dicionário que mapeia docid para uma lista de tokens.
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        
    Returns:
        Uma lista com os documentos ordenados.
    '''
    rank = {}

    for docid in docids:
        points = 0
        
        for word in repo[docid]:
            freq = index[word][docid]
            ni = len(index[word].keys())
            n = len(repo.keys())

            points += (1+math.log2(freq))*math.log2(n/ni)

        rank[docid] = points/len(repo[docid])
        
    return rank


def n_rank(query, docids, index, repo):
    '''Utiliza a contamge de palavras para favorecer um texto que tem as mais
    palavras da quey

    Args:
        docids: lista de documentos para avaliar
        repo: Um dicionário que mapeia docid para uma lista de tokens.
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        
    Returns:
        Uma lista com os documentos ordenados.
    '''
    filtered_query = query.replace("(", "").replace(")","").split(" ")
    
    rank = defaultdict(int)
    n_words = defaultdict(int)
    
    for word in filtered_query:
        if word in index.keys():
            for docid in index[word].keys():
                if docid in docids:
                    n_words[docid] += 1
        
    rank = {docid:(n_words[docid]/len(filtered_query)) for docid in docids}
    
    return rank


def semantic_rank(query, docids, index, repo):
    '''Utiliza a classe da palvras da query par verificar qual documento tem as 
    mais palavras do tip ogramatica mais importante no texto

    Args:
        query: string com as plavras que o documento deve conter
        repo: Um dicionário que mapeia docid para uma lista de tokens.
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        docids: lista de documentos para avaliar
        
    Returns:
        Uma lista com os documentos ordenados.
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
    
    filtered_query = query.replace("(", "").replace(")","").split(" ")
    tags = (tagger(filtered_query))
    tags = {key: points[translator[value]]*2 for key, value in tags}
    
    rank = defaultdict(int)
    n_words = defaultdict(int)
    
    for word in filtered_query:
        if word in index.keys():
            for docid in index[word].keys():
                if docid in docids:
                    rank[docid] += tags[word] * index[word][docid]
                    n_words[docid] += index[word][docid]
        
    rank = {docid:(rank[docid]/n_words[docid] if n_words[docid] != 0 else 0) for docid in docids}
    
    return rank
        
    