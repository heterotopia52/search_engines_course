import requests
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


def fetch_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Κάτι πήγε λάθος"
    elif response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


def index_words(soup):
    index = {}
    words = re.findall(r'\b\w+\b', soup.get_text())
    for word in words:
        word = word.lower()
        if word in index:
            index[word] += 1
        else:
            index[word] = 1
    return index


def remove_stop_words(index):
    stop_words = ['a', 'about', 'above', 'after', 'again',
                  'against', 'all', 'am', 'an', 'and',
                  'any', 'are', "aren't", "or", "in",
                  "on", "at", 'as', 'at', 'be', 'because',
                  'been', 'before', 'being', 'below',
                  'Ο', 'η', 'το', 'του', 'της', 'των', 'τον', 'την', 'τα', 
                  'τις', 'τους', 'τι', 'ποιος', 'ποια', 'ποιο',
                  'τους', 'τι', 'ποιος', 'ποια', 'ποιο',
                  'ποιοι', 'ποιες', 'ποιων', 'ποιους', 'ποιες', 
                  'ποιαν', 'ποιον', 'σε', 'στο', 'στη', 
                  'στα', 'στις', 'στου']
    for stop_words in stop_words:
        if stop_words in index:
            del index[stop_words]
    return index


def apply_stemming(index):
    stemmer = PorterStemmer()
    stemmed_index = {}
    for word, count in index.items():
        stemmed_word = stemmer.stem(word)
        if stemmed_word in stemmed_index:
            stemmed_index[stemmed_word] += count
        else:
            stemmed_index[stemmed_word] = count
    return stemmed_index


def search(query, index):
    query = query.lower()
    if query in index:
        return index[query]
    else:
        return "Ο όρος δεν βρέθηκε"
    query_words = re.findall(r'\b\w+\b', query)
    results = {}
    for word in query_words:
        if word in index:
            results[word] = index[word]
    return results


def search_engine(url, query):
    soup = fetch_page(url)
    if soup is None:
        return "Κάτι πήγε στραβά"
    index = index_words(soup)
    index = remove_stop_words(index)
    index = apply_stemming(index)
    results = search(query, index)
    return results


search_prompt = "Δώστε τον όρο αναζήτησής σας: "
query = input(search_prompt)
url_prompt = "Δώστε το URL της σελίδας που θέλετε να αναζητήσετε: "
url = input(url_prompt)
search_result = search_engine(url, query)
print(f"Ο όρος '{query}' που δώσατε βρέθηκε {search_result} φορές")
