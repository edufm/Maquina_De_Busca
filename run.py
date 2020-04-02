from argparse import ArgumentParser
import search_engine as se

def main():
    parser = ArgumentParser()
    parser.add_argument('target_corpus', 
                        help='Arquivo json com um dicionario docid para texto'
                        ,type= str, default= "reuters", nargs='?')
    
    parser.add_argument('query', 
                        help='Arquivo json com um dicionario docid para texto',
                        type= str, default= "(asian (US rise)) (export banana)", nargs='?')
    
    parser.add_argument('DO_SETUP', 
                        help='Arquivo json com um dicionario docid para texto',
                        type= bool, default= False, nargs='?')

    parser.add_argument('TEST_MODE', 
                        help='Arquivo json com um dicionario docid para texto',
                        type= bool, default= True, nargs='?')

    args = parser.parse_args()
    print(args)

    corpus_file = (f"./storage/corpus_{args.target_corpus}_mini" if(args.TEST_MODE) else f"./storage/corpus_{args.target_corpus}")
    repo_file   = f"./storage/repo_{args.target_corpus}"
    index_file  = f"./storage/index_{args.target_corpus}"
    
    # ---------------------------- Setup do Repo ----------------------------------
    if args.DO_SETUP:
        # Cria o corpus
        se.gera_corpus.run(args.target_corpus)
        
        # Cria o repo e indice
        se.indexador.run(args.target_corpus, corpus_file)
        
    # Lê o repo
    repo = se.repository.load(repo_file)
    
    # Lê o indice
    index = se.repository.load(index_file)
    
    
    # -------------------------------- Querys -------------------------------------
    naive_results = list(se.search.naive_search(index, args.query))
    and_or_results = list(se.search.and_or_search(index, repo, args.query))
    busca_results = list(se.search.busca_docids(index, args.query))

    rank = se.search.rank(and_or_results, index, repo)
    print(f"rank:{rank}")


    print({"naive_results":naive_results,
        "and_or_results":and_or_results,
        "busca_results" :busca_results})

if __name__ == '__main__':
    main()