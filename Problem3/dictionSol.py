from ast import Pass
import json

import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet




def get_page_words(page_url):
    """get the words from a page using its url
       The beautifulSoup function helps us scrap html data from the page 
       Then I removed all the symbols from all the words 

       I looped through the words to get the mode of each word while checking it is english or not
       I did this by using a library called nltk.corpus.wordnet and placed the non-english words in a new list


        Args:
            page_url(string): This is the a string of the page url.
        Returns:
            {
                'all_words': list of all unique words,
                'non_english': list of all non-english words),
                'word_count': mode of all unique words,
            }

        

    """
    page = requests.get(page_url).text
    soup = BeautifulSoup(page, 'html.parser')
    all_words = []
    non_english = []
    word_count = dict()

    for each_text in soup.find_all('p'):
        content = each_text.text
        p_words = content.lower().split()
        p_non_english_words = []
        for index, word in enumerate(p_words):
            symbols = " !@#$%^&*()_-+={[}]|\\;:\"<>?/.,"
            for symbol in symbols:
                if symbol in word:
                    word = word.replace(symbol, '')
            p_words[index] = word

            # update word count
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
            # check if word is an english word
            if not is_english_word(word):
                p_words.remove(word)
                p_non_english_words.append(word)
        all_words += p_words
        non_english += p_non_english_words
        
    
    return {
        'all_words': list(set(all_words)),
        'non_english': list(set(non_english)),
        'word_count': word_count,
        
    }


def is_english_word(name):
    """ Check if a word is english or not

    Args:
            name(string): word to be evaluated.
    Returns:
        bool: The return value. True if word is english, False otherwise.

    """
    return bool(wordnet.synsets(name))


def compare_the_two(page_words1, page_words2):
    """Compares pages
    get words unique to page 1 and 2 respectively
    get duplicate words in both pages
    Args:
        page_words1 (dict): {
                'all_words': list of all unique words,
                'non_english': list of all non-english words),
                'word_count': mode of all unique words,
            }

        page_words2 (dict): {
                'all_words': list of all unique words,
                'non_english': list of all non-english words),
                'word_count': mode of all unique words,
            }
    
    
    """
    set_words1 = set(page_words1['all_words'])
    set_words2 = set(page_words2['all_words'])
    #keep only duplicate

    set_words1.intersection(set_words2)

    #unique words in page one
    unique_words_in_page_one = set_words2.difference(set_words1)
    
    #unique words in page two
    unique_words_in_second_page = set_words1.difference(set_words2)
    
    return{
        'duplicate words in both pages':list(set_words1),
        'unique words in page one':list(unique_words_in_page_one),
        'unique words in page two' : list(unique_words_in_second_page)
    }

def main():
    page_url = input("Enter the URL of the first page")
    page_words1 = get_page_words(page_url)
    compare = input('Do you want to compare with another page?')
    if compare == 'Yes':
        page_url = input("Enter the URL of the second page")
        page_words2 = get_page_words(page_url)


    print('all words in first page')
    print(json.dumps(page_words1, indent=3))

    print('two')
    print(json.dumps(page_words2, indent=3))

    print("compare the two pages")
    print(json.dumps(compare_the_two(page_words1, page_words2), indent=3))

if __name__ == '__main__':
    main()