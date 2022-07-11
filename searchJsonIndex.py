import nltk, json, time
from nltk.corpus import stopwords


# nltk.download('stopwords')
ps = nltk.PorterStemmer()
stops = set(stopwords.words('english'))


def load_index():
    # loads the inverted index from a json file depending on user input
    print('\nLoading Search Engine...\n')
    index = json.load(open('tfidfJsonIndex.json'))
    return index


def prompt_for_query():
    # prompts console for input query
    prompt_query = input('Search: ')
    query_list = []
    tokens = nltk.word_tokenize(prompt_query)
    for t in tokens:
        stem = ps.stem(t, True)
        if t.isalnum() and t not in stops:
            query_list.append(stem)
    return query_list


def search_index(query_list, index):
    # looks up query keywords in index and returns subset of index with keywords
    searched_dict = {}
    for query in query_list:
        if query in index.keys():
            for url, value in index[query].items():
                if url not in searched_dict:
                    searched_dict[url] = value
    return searched_dict


def ranked_top_five(searched_dict):
    # returns top 5 ranked URLs based on original search query
    ranked = sorted(searched_dict.items(), key=lambda x: -int(x[1]))
    top_5_urls = [x[0] for x in ranked[:5]]
    return top_5_urls


if __name__ == '__main__':
    inverted_index = load_index()
    for i in range(1):
        prompt = prompt_for_query()
        if not prompt:
            print('Your search did not match any documents.')
        start = time.time()
        r = search_index(prompt, inverted_index)
        print('Top 5 Results:')
        for result in ranked_top_five(r):
            print(result)
        print(f'Search time: {round(time.time() - start, 10)} seconds')

