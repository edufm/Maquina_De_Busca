import search_engine.repository as rp
 
def run(target, corpus_file):
    corpus = rp.load(corpus_file)
    repo   = rp.create_repo(corpus)
    index  = rp.create_index(repo)
    
    rp.save(repo, f'./storage/repo_{target}')
    rp.save(index, f'./storage/index_{target}')
