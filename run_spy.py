import search_engine as se

target_corpus = "reuters"
query = "(asian us malasyan) (export (send goods))"
DOSETUP = True
TESTMODE = True

corpus_file = (f"./storage/corpus_{target_corpus}_mini.json" if(TESTMODE) else f"./storage/corpus_{target_corpus}.json")
repo_file   = f"./storage/repo_{target_corpus}.json"
index_file  = f"./storage/index_{target_corpus}.json"

stopwords = (True, "freq")
normalize=(True, "lower")

# ---------------------------- Setup do Repo ----------------------------------
if DOSETUP:
    # Cria o corpus
    se.gera_corpus.run(target_corpus, file=corpus_file, TESTMODE=TESTMODE)
    
    # Cria o repo e indice
    se.indexador.run(target_corpus, corpus_file, repo_file=repo_file, index_file=index_file,
                     stopwords=stopwords, normalize=normalize)
    
# Lê o corpus
corpus = se.repository.load(corpus_file)    

# Lê o repo
repo = se.repository.load(repo_file)

# Lê o indice
index = se.repository.load(index_file)


# -------------------------------- Querys -------------------------------------
docids = list(se.search.busca_docids(index, query))

rank = se.search.rank(docids, index, repo)

if len(rank) > 0:
    print(rank)
    print()
    print()
    for docid in rank:
        print(corpus[docid])
        print()
        print()
else:
    print("No match for query")