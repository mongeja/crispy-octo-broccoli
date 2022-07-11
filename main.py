import os, json, nltk, csv, time, re
from collections import defaultdict
from gettext import install
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import lxml

# Stemming words with nltk library
ps = nltk.PorterStemmer()


def gen_token_dict(s, new_token):
    title_url_token = new_token
    tokens = nltk.word_tokenize(s)          # tokenize the word/token
    token_dict = defaultdict(int)           # create a sub-class dictionary
    for t in tokens:
        if t.isalnum():                     # check each token whether it is alphanumeric
            stem = ps.stem(t, True)         # stem the word to its root word
            token_dict[stem] += 1

    for i in title_url_token:
        if i in token_dict:
            token_dict[i] = token_dict[i] * 2
    # print(token_dict)
    return token_dict                        # return the sub-class dictionary of token_dict

def title_url(s):
    title = s.find_all(('h1'))
    tokens = []
    for i in title:
        tokens.append(str(i))
    new_tokens = []
    for i in tokens:
        for small_token in re.split(r'(\W+)+', i):
            if small_token.isalnum():
                eachWord = small_token.lower()
                new_tokens.append(eachWord)
    new_tokens = remove_duplicate_title(new_tokens)
    # print(new_tokens)
    return new_tokens

def remove_duplicate_title(list):
    res = []
    for i in list:
        if i not in res:
            res.append(i)
    return res

def add_to_index(index, post_dict):
    for url, tkd in post_dict.items():
        o = urlparse(url)
        unique_url = o._replace(fragment='').geturl()                      # discard fragment
        for term, frequency in tkd.items():
            if term not in index:
                index[term] = [unique_url, frequency]
            else:
                index[term].append(unique_url)
                index[term].append(frequency)

def transform_list(lis):
    # takes a list argument and returns list of tuples sorted by frequency
    # [(url, n),  (url, n), ...]
    tup_list = []
    for i in range(0, len(lis)-1, 2):
        pair = (lis[i], lis[i+1])
        tup_list.append(pair)
    sorted_tups = sorted(tup_list, key=lambda x: -int(x[1]))
    return sorted_tups

def write_to_file(index):
    file = open('Newjsonfile.json', 'w')
    index_write = {}
    post = []
    for term, post_list in index.items():
        token = term
        post = post_list
        url_freq = transform_list(post[2:])                 # write to json file
        index_write[token] = url_freq
    file.write(json.dumps(index_write))
    return index_write

def prompt_for_query(prompt):
    query_list = []
    tokens = nltk.word_tokenize(prompt)
    for t in tokens:
        if t.isalnum():
            stem = ps.stem(t, True)
            query_list.append(stem)
    return query_list


def search_index(query_list, index):
    # looks up query keywords in index and returns list of relevant entries
    searched_list = []
    for query in query_list:
        if query in index.keys():
            for q in index[query]:
                searched_list.append(q)
    return searched_list

def remove_duplicate(relevant_url):
    res_list = []
    for i in range(len(relevant_url)):
        if relevant_url[i] not in relevant_url[i + 1:]:  # because when we remove fragment, the url become the same. Try go to see these two
            res_list.append(relevant_url[i])             # https://www.informatics.uci.edu/explore/faculty-profiles/cristina-lopes/#content
    return res_list                                      # https://www.informatics.uci.edu/explore/faculty-profiles/cristina-lopes/


def ranked_top_five(relevant_urls):
    # returns top 5 ranked URLs based on original search query
    uniqueness = remove_duplicate(relevant_urls)
    ranked = sorted(uniqueness, key=lambda x: -int(x[1]))[:5]
    top_5_urls = [x[0] for x in ranked]
    return top_5_urls

if __name__ == "__main__":
    inverted_index = {}
    root_dir = os.getcwd()                   # assign the current working directory
    os.chdir("ANALYST")                      # changes the current working directory to the 'ANALYST' path
    analyst_dir = os.getcwd()                # assign the current working directory
    analyst_folder = os.listdir()            # assign the list of all files and directories in the specified directory
    for f in analyst_folder:
        os.chdir(f)
        print(os.getcwd())
        file_list = os.listdir()
        for js in file_list:
            postings = {}
            js_dict = json.load(open(js))   # open json file then take a file object and returns the json object
            # soup = BeautifulSoup(js_dict['content'], 'html.parser')
            soup = BeautifulSoup(js_dict['content'], "xml")
            new_token = title_url(soup)
            tkn_dict = gen_token_dict(js_dict['content'], new_token)  # call function to tokenize the content
            postings[js_dict['url']] = tkn_dict            # assign the dictionary of token
            add_to_index(inverted_index, postings)
        os.chdir(analyst_dir)
    os.chdir(root_dir)
    ind = write_to_file(inverted_index)
    num = 0
    while num < 21:
        # prompts console for input query
        prompt = input('Search: ')
        start1 = time.time()
        query = prompt_for_query(prompt)
        r = search_index(query, ind)
        for url in ranked_top_five(r):
            print(url)
        print(time.time() - start1)
        num = num + 1