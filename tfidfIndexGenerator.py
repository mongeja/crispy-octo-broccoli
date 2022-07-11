import os, json, nltk, math
from collections import defaultdict
from urllib import parse


ps = nltk.PorterStemmer()


def gen_token_dict(docstr):
    # parses through a string and tokenizes alphanumeric words using nltk
    # library. returns a frequency dictionary of the tokens.
    token_dict = defaultdict(int)
    tokenized_list = nltk.word_tokenize(docstr)
    for token in tokenized_list:
        if token.isalnum():
            stem = ps.stem(token, True)
            token_dict[stem] += 1
    return token_dict


def gen_tf_dict(token_dict):
    # creates a dict from the token frequency and logarithmizes the number of
    # occurences of the token in the document
    tf_dict = {t: 1 + math.log(c, 10) for t, c in token_dict.items()}
    return tf_dict


def add_to_index(index, post_dict):
    # takes in a dictionary of postings and stores them in an inverted index
    # with the tokens as the keys
    for url, tkd in post_dict.items():
        for term, val in tkd.items():
            posting = {url: val}
            if term not in index:
                index[term] = posting
            else:
                index[term] = {**index[term], **posting}


def gen_tfidf_dict(index, total_docs):
    # calculates the idf value from the original index and then generates a
    # new index replacing tf values with the respective tf-idf scores
    tfidf_dict = {}
    for term, postings_dict in index.items():
        doc_freq = len(postings_dict)
        if doc_freq == 0:
            doc_freq = 1
        idf = math.log(total_docs / doc_freq, 10)
        tfidf_dict[term] = {url: round(tf * idf, 6) for url, tf in postings_dict.items()}
    return tfidf_dict


def write_to_file(index):
    # writes data from the inverted index to a json file
    json.dump(index, open('tfidfJsonIndex.json', 'w'))


if __name__ == "__main__":
    inverted_index = {}
    doc_count = 0  # counts total number of documents to be parsed for idf

    root_dir = os.getcwd()
    os.chdir("ANALYST")
    analyst_dir = os.getcwd()
    analyst_folder = os.listdir()

    for f in analyst_folder:
        os.chdir(f)
        print(os.getcwd())
        file_list = os.listdir()

        # this part parses through each json file and collects the data using
        # the above functions
        for js in file_list:
            js_dict = json.load(open(js))
            doc_count += 1
            postings = {}

            # removing 'duplicate' entries due to url fragments
            defragged_url = parse.urldefrag(js_dict['url'])[0]
            tk_count = gen_token_dict(js_dict['content'])
            tf_score = gen_tf_dict(tk_count)
            postings[defragged_url] = tf_score
            add_to_index(inverted_index, postings)

        os.chdir(analyst_dir)
    os.chdir(root_dir)
    tfidf_scores = gen_tfidf_dict(inverted_index, doc_count)
    write_to_file(tfidf_scores)
