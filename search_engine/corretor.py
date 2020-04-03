from nltk.corpus import wordnet

def dist1(term):
    '''Cria uma lista com todas os termos com distância de edição 1 para o termo recebido

    Args:
        term: palavra que se deseja propagar
    
    Returns:
        Uma lista com os termos de  distancia 1.
    '''    
    letters = "abcdefghijklmnopqrstuvwxyz"
    split   = [(term[:i], term[i:]) for i in range(len(term))] 
    
    delete  = [L[:] + R[1:] for (L,R) in split]
    insert  = [L + c +  R for L,R in split for c in letters]
    replace = [L + c + R[1:] for L,R in split for c in letters]

    return delete + insert + replace 


def dist2(ed1):
    '''Cria uma lista com todas os termos com distância de edição 1 para 
       os termos que ja tem distancia 1 recebidos

    Args:
        ed1: termos com distancia de edição 1
    
    Returns:
        Uma lista com os termos de  distancia 2.
    '''
    ed2 = set()
    for word in ed1:
        ed2.update(dist1(word))
    
    return ed2


def run(word, vocab):
    '''realiza a correção da palavra para a palavra do vocubalario com menor 
       distancia de edição

    Args:
        word: palavra a ser corrigida
        vocab: palavras existentes
    
    Returns:
        Palavra corrigida
    '''
    if(word in vocab):
        return word

    ed1 = dist1(word)
    for w in ed1:
        if(w) in vocab:
            return w
    
    for w in dist2(ed1):
        if(w) in vocab:
            return w
        
    return word


def synonims(word):
    '''Busca todos os sinonimos de uma palara com o wordnet

    Args:
        word: palavras para a qual os sinonimos devem ser enontrados
    
    Returns:
        lista de sinonimos
    '''
    synonims = set(w.lemmas()[0].name() for w in wordnet.synsets(word))
    
    return synonims