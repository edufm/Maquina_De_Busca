import search_engine.repository as rp
 
def run(target, corpus_file, repo_file=None, index_file=None,
        stopwords=(True, "preset"), normalize=(True, "lower")):
    '''Cria o index e um repositório a partir de um corpus previamente filtrado

    Args:
        target: Corpo alvo do NLTK
        corpus_file: nome do arquivo de entrada do corpus
        repo_file: nome do arquivo de saida do repo
        index_file: nome do arquivo de saida do index
        
        stopwords: argumentos do create_repo, verificar documentação da função
        do_normalize: argumentos do create_repo, verificar documentação da função
        
    Returns:
        Um dicionario que tem os dados do corpus
    '''
    # Verifica se o usuario passou um file customizado, se não, cria um padrão
    if repo_file == None:
        repo_file = f"./storage/repo_{target}.json"
    if index_file == None:
        index_file = f"./storage/index_{target}.json"
    
    # Abre o corpus
    corpus = rp.load(corpus_file)
    
    # Gera os dados necessarios
    repo   = rp.create_repo(corpus, stopwords=stopwords, normalize=normalize)
    index  = rp.create_index(repo)
    #semantic_index = rp.create_type_index(repo)
    
    # Salva os dicinarios gerados
    rp.save(repo, repo_file)
    rp.save(index, index_file)