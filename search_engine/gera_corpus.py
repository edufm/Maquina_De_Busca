import json
from nltk.corpus import reuters

def run(target="reuters"):
    '''Cria o corpus a partir do NLTK

    Args:
        target: Corpo alvo do NLTK
        filename: nome do arquivo de saida para o corpus
    
    Returns:
        Um dicionario que tem os dados do corpus
    '''

    corpus = {"reuters": reuters}
    
    if(not corpus[target]) :
        raise Exception(f"Corpus {target} not implemented yet")
    
    docs = {}
    for fileid in corpus[target].fileids():
        docs[fileid] = corpus[target].raw(fileid)

    mini_docs = {k: docs[k] for k in list(docs)[:10]}
    
    with open(f"./storage/corpus_{target}.json", 'w') as file:
        json.dump(docs, file, indent=4)

    with open(f"./storage/corpus_{target}_mini.json", 'w') as file:
        json.dump(mini_docs, file, indent=4)
