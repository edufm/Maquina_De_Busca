import search_engine

# --------------------------- Inputs do usuario -------------------------------
TEST_MODE = True
DO_SETUP = True
# Inputs vinculados ao Setup
target_corpus = "reuters"
corpus_file = "./storage/corpus_reuters"
repo_file = "./storage/repo_reuters"
index_file = "./storage/index_reuters"
# Inputs vinculados a query
query = "(asian US) (export banana)"

# ---------------------------- Setup do Repo ----------------------------------
if DO_SETUP:
    # Cria o corpus
    corpus = search_engine.repository.create_corpus(target_corpus)
    search_engine.repository.save_corpus(corpus, corpus_file)
    
    if TEST_MODE:
        corpus = {k: corpus[k] for k in list(corpus)[:10]}
        search_engine.repository.save_corpus(corpus, f"{corpus_file}_mini")
        
    # Cria o repo
    repo = search_engine.repository.create_repo(corpus)
    search_engine.repository.save_repo(repo, repo_file)
    
    # Cria o indice
    index = search_engine.repository.create_index(repo)
    search_engine.repository.save_index(index, index_file)
    
else:
    # Lê o corpus
    corpus = search_engine.repository.load_corpus(corpus_file)
    
    if TEST_MODE:
        corpus = {k: corpus[k] for k in list(corpus)[:10]}
        
    # Lê o repo
    repo = search_engine.repository.load_repo(repo_file)
    
    # Lê o indice
    index = search_engine.repository.load_index(index_file)
    
# -------------------------------- Querys -------------------------------------
naive_results = list(search_engine.search.naive_search(index, repo, query))
    
and_or_results = list(search_engine.search.and_or_search(index, repo, query))

print({"naive_results":naive_results,
       "and_or_results":and_or_results})