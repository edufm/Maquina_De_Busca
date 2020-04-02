
#from nlt.metrics import edit_distance
from nltk.corpus import wordnet

#wordnet.synsets - > facil xbugado
#sinonimos 
#Rank -> alto
#palavas populares - >

def dist1(term):
    letters = "abcdefghijklmnopqrstuvwxyz"
    split   = [(term[:i], term[i:]) for i in range(len(term))] 
    
    delete  = [L[:] + R[1:] for (L,R) in split]
    insert  = [L + c +  R for L,R in split for c in letters]
    replace = [L + c + R[1:] for L,R in split for c in letters]

    return delete + insert + replace 


def dist2(ed1):
    ed2 = set()
    for word in ed1:
        ed2.update(dist1(word))
    
    return ed2


def similarity(word):
    words = set(w.lemmas()[0].name() for w in wordnet.synsets(word))


def run(word, vocab):
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
