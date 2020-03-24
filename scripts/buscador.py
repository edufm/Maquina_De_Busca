import json
from argparse import ArgumentParser
from collections import defaultdict

def busca(index, repo, query):
    # Parsing da query.

    # Recuperar os ids de documento que contem todos os termos da query.
    score = []
    for word in query.split(" "):
        score.append(set(index[word].keys()))

    # Retornar os textos destes documentos.
    results = score[0]
    for result in score[1:]:
        results = results.intersection(result)
    
    return [repo[r] for r in results]

def main():
    parser = ArgumentParser()
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)

    test = busca(index, repo, args.query)
    print(test)

if __name__ == '__main__':
    main()
