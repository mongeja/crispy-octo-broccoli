Authors: Henry Tran, Davy Nguyen, Ly Heng Teng, Jenelle Monge

This document belongs in a zip folder containing the following files: 'main.py', 'tfidfIndexGenerator.py', 'searchJsonIndex.py', 'TEST.txt', and 'README.txt' (this document).
----------------------------------------------------------------------
Definitions:
'main.py' WARNING: it is our first attempt at this assignment and is only included for performance comparison purposes; it takes several minutes to parse through all the json files and several seconds to retrieve queries in the search engine. The latter programs described in the instructions below represent our final optimized search engine.

'tfidfIndexGenerator.py' is a script that generates an inverted index of tokens and their corresponding postings. Each posting contains the url of the document in which the token was found and the token's tf-idf score for that document. The generated data structure is stored as a json file named 'tfidfJsonIndex.json' in the working directory.

'searchJsonIndex.py' is a program that runs our search engine's interface within the console. It prompts the user to select the TF index or the TF-IDF index. It loads the appropriate search engine and then prompts the user for a search query.

'TEST.txt' is a text file containing all the queries we used to measure the performance of our search engine.

'README.txt' is this currently open document. It contains the definitions of each file and the instructions on how to run our search engine.
----------------------------------------------------------------------
Instructions:
1. Run the 'tfidfJsonIndex.py' script.
2. After the script has completed and the file 'tfidfJsonIndex.json' has been generated, run the 'searchJsonIndex.py' program.
3. Enter query inputs from 'TEXT.txt' or any string of text for the engine to search through the index and retrieve the relevant urls.
