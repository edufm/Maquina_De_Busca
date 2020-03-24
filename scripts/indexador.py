import json
import nltk
import re


from argparse import ArgumentParser
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def create_repo(corpus, stop_words=True, normalize=True, subs=True):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    nltk.download('stopwords')
    
    repo = {}
  
    for docid, text in corpus.items():

        text = re.sub(r"[^a-zA-Z0-9 ]", "", text, flags=re.DOTALL|re.MULTILINE)
        text_tokens = word_tokenize(text)
        if(stop_words):
            text_tokens = [word for word in text_tokens if not word in stopwords.words()]
        
        #if(subs):
        #    text_tokens = [word for word in text_tokens if 'NN' in nltk.pos_tag(word)[1]]
        
        if(normalize):
            text_tokens = [PorterStemmer().stem(word) for word in text_tokens]

        repo[docid] = text_tokens


        
    return repo

def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''

    indexed = defaultdict(lambda:defaultdict(int))
    for doc_id, words in repo.items():
        for word in words:
            indexed[word][doc_id] +=1

    return indexed

def main():
    parser = ArgumentParser()
    parser.add_argument('corpus',
                        help='Arquivo json com um dicionario docid para texto')
    parser.add_argument('repo_name',
                        help='Raiz do nome do arquivo de repositorio')
    args = parser.parse_args()

    with open(args.corpus, 'r') as file_corpus:
        corpus = json.load(file_corpus)

    repo = create_repo(corpus)
    index = create_index(repo)

    with open(args.repo_name + '_repo.json', 'w') as file_repo:
        json.dump(repo, file_repo, indent=4)

    with open(args.repo_name + '_index.json', 'w') as file_index:
        json.dump(index, file_index, indent=4)


if __name__ == '__main__':
    main()
