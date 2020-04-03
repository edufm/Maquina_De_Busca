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
    
    parser.add_argument('DOSETUP', 
                        help='Arquivo json com um dicionario docid para texto',
                        type= bool, default= False, nargs='?')

    parser.add_argument('TESTMODE', 
                        help='Arquivo json com um dicionario docid para texto',
                        type= bool, default= True, nargs='?')

    args = parser.parse_args()
    print(args)

    corpus_file = (f"./storage/corpus_{args.target_corpus}_mini" if(args.TEST_MODE) else f"./storage/corpus_{args.target_corpus}")
    repo_file   = f"./storage/repo_{args.target_corpus}"
    index_file  = f"./storage/index_{args.target_corpus}"
	
	stopwords = (True, "freq")
	normalize=(True, "lower")
    
	# ---------------------------- Setup do Repo ----------------------------------
	if args.DOSETUP:
		# Cria o corpus
		se.gera_corpus.run(args.target_corpus, file=corpus_file, TESTMODE=args.TESTMODE)
		
		# Cria o repo e indice
		se.indexador.run(args.target_corpus, corpus_file, repo_file=repo_file, index_file=index_file,
						 stopwords=stopwords, normalize=normalize)
		
	# Lê o corpus
	corpus = se.repository.load(corpus_file)    

	# Lê o repo
	repo = se.repository.load(repo_file)

	# Lê o indice
	index = se.repository.load(index_file)


	# -------------------------------- Querys -------------------------------------
	docids = list(se.search.busca_docids(index, args.query))

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

if __name__ == '__main__':
    main()