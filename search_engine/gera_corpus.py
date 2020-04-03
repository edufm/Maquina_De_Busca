import json
from nltk.corpus import reuters

def run(target, file=None, TESTMODE=False):
    '''Cria o corpus a partir do NLTK

    Args:
        target: Corpo alvo do NLTK
        file: nome do arquivo de saida para o corpus
        TESTMODE: boleana para dizer se o corpus deve ser gerado por completo ou apenas uma versão mini
    
    Returns:
        Um dicionario que tem os dados do corpus
    '''
    
    # Verifica se o usuario passou um file customizado, se não, cria um padrão
    if file == None:
        if TESTMODE:
            file = f"./storage/corpus_{target}_mini.json"
        else:
            file = f"./storage/corpus_{target}.json"

    # Verifica se o corpus selecionado estará disponivel para leitura
    corpus = {"reuters": reuters}
    if not target in corpus.keys():
        raise Exception(f"Corpus {target} not implemented yet")
    
    # Gera o arquivo Corpus
    if TESTMODE:
        docs = {}
        for fileid in corpus[target].fileids()[:10]:
            docs[fileid] = corpus[target].raw(fileid)
         
        with open(file, 'w') as file:
            json.dump(docs, file, indent=4)
        
    else:
        docs = {}
        for fileid in corpus[target].fileids():
            docs[fileid] = corpus[target].raw(fileid)
            
        with open(file, 'w') as file:
            json.dump(docs, file, indent=4)

 
