'''Funções para realzação dos diferentes tipos de busca
'''
import re

def naive_search(index, repo, query):
    '''Executa uma query que exige o texto conter todas as palavras.

    Args:
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        repo: dicionario que mapeia docid para uma lista de tokens.
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
            return []       
    # Retornar os textos destes documentos.
    results = score[0]
    for result in score[1:]:
        results = results.intersection(result)
    
    return results


def and_or_search(index, repo, query):
    '''Executa uma query que exige o texto conter as palavras da query com 
    logica "E" (sem parenteses) ou "ou" (entre parenteses).

    Args:
        index: dicionario que mapeia palavra para um dicionario que mapeia 
                docids para a contagem dessa palavra no documento.
        repo: dicionario que mapeia docid para uma lista de tokens.
        query: string com as plavras que o documento deve conter
        
    Returns:
        Uma lista com os documentos selecionados.
    '''
    # Verifica as palavras na query
    split_query = list(map(lambda x: x.strip("()"), query.split(" ")))
        
    # Processa a query para ver onde estão os "ors"
    ors = []
    ors_loc = {}
    for  n, char in enumerate(query):
        
        if char == "(":
            start = n
        elif char == ")":
            end = n
            # Guarda cada pavra do or e sua posição
            ors.append(query[start+1:end].split(" "))
            for word in ors[-1]:
                ors_loc[word] = len(ors)-1
    
    # Itera as palavras da query para ver em que texto aprecem
    score = []
    done = []
    available_words = index.keys()
    for word in split_query:
        # Verifica se a palavra ja havia sido feita (em um or por exemplo)
        if word not in done:
            # Processa a palavra que estão em um "or"
            if word in ors_loc.keys():
                # Pega o score para a primeira palavra e verifica quais outras palavras estão no or
                if not word in available_words:
                    this_score = set()
                else:
                    this_score = set(index[word].keys())                
                or_words = ors[ors_loc[word]]
                or_words.remove(word)
                # Itera o restante das palavras e adiciona ao score
                for or_word in ors[ors_loc[word]]:
                    if not or_word in available_words:
                        this_score = this_score.union(set())
                    else:
                        this_score = this_score.union(set(index[or_word].keys()))
                    done.append(or_word)
                    
            # Processa a palavra que não estão em um "or"
            else:
                this_score = set(index[word].keys())
    
            score.append(this_score)
        
    # Faz a intersecção de todos os scores
    results = set.intersection(*score)
        
    return results