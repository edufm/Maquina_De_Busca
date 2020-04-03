'''Funções para realzação dos diferentes tipos de busca
'''
import re
import math
from search_engine import corretor
from nltk.tokenize import sexpr_tokenize

def strip_parenthesis(query):
    
    if query[0] == "(":
        query = query[1:]
    if query[-1] == ")":
        query = query[:-1]
    
    return query.lower()


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
    queries = [strip_parenthesis(q) for q in sexpr_tokenize(query)]
    results = []
    for sub_query in queries:

        if "(" in sub_query:
            sub_docids = busca_docids(index, sub_query, in_sub_query=True)
        
        else:
            if use_corretor:
                split_query = [corretor.run(word, list(index.keys())) for word in sub_query.split(" ")]
                sub_query = " "
                sub_query = sub_query.join(split_query).strip(" ")
            
            sub_docids = or_search(index, sub_query)
        
        results.append(set(sub_docids))

    if in_sub_query:
        docids = set.union(*results)
    else:
        docids = set.intersection(*results)
    
    return docids


def or_search(index, query):
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
    results = score[0]
    for result in score[1:]:
        results = results.union(result)
    
    return results


def rank(docids, index, repo):
    '''Utiliza o TF-IDF para verificar quais documentos tem mais palavras incomuns

    Args:
        repo: Um dicionário que mapeia docid para uma lista de tokens.
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        docides: lista de documentos para avaliar
        
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
        
    return [k for k, v in sorted(rank.items(), key=lambda item: item[1])]
    