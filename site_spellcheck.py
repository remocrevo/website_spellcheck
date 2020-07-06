# scrape all web pages of a website
# - this might be easiest with wget
# remove HTML tags
# spellcheck the rest of the text
# print out any misspelled words with their web page URL

# dependencies
# - wget, with recent version of openssl: https://eternallybored.org/misc/wget/

import sys
import os
import re
from bs4 import BeautifulSoup
from spellchecker import SpellChecker

# returns only text, removes HTML tags
def get_text_from_html_file(filename):
    # read html file, send it through beautifulsoup
    file = open(filename, "r") 
    html_contents = file.read()
    soup = BeautifulSoup(html_contents, features="html.parser")
    text = soup.get_text()
    #print(text)
    return text

# spell check with something like pyspellchecker
# - finds 'hapenning', 'herre', 'Drupal'
# - doesn't find crazy long words
def spellcheck(words):
    spell = SpellChecker(distance=1)

    # make sure some words are not flagged as misspelled
    spell.word_frequency.load_words(['\n', '©', 'blog', 'website', 'monetization', 'php', 'analytics', 'seo', 'wordpress', 'mysql', 'html5', 'css3', 'google', 'drupal', 'facebook', 'youtube', 'linkedin'])

    # find those words that may be misspelled
    misspelled = spell.unknown(words)

    results = []
    for word in misspelled:
        # Get the one `most likely` answer
        #suggestion = spell.correction(word)
        results.append(word)

    return results

def find_repeated_words(words):
    repeated = []
    prev_word = ''
    for word in words:
        if word == prev_word:
            repeated.append(word)

        prev_word = word

    return repeated




# read in home page URL
domain = sys.argv[1]
start_url = sys.argv[1]

# download all of the HTML pages (but no images/scripts) for a website
# XXX: This wget command still downloads CSS/Javascript/images
# TODO: FIRST, check if dir already exists, or ask "this might take a while. Are you sure?"
os.system('wget --recursive --no-clobber --html-extension --restrict-file-names=windows --domains %s --no-parent --wait=5 %s --no-check-certificate' % (domain, start_url))

# change into site dir made by wget
os.chdir(domain)

# FIND ALL HTML FILES, RECURSIVELY
# r=>root, d=>directories, f=>files
for r, d, f in os.walk('.'):
    for item in f:
        if '.html' in item:
            filename = os.path.join(r, item)
            text = get_text_from_html_file(filename)
            # replace ending punctuation with spaces
            punct = re.compile('[:!,\.\?\/]')
            text = punct.sub(' ', text)
            
            # output the filename so we know where the incorrect words live
            print(filename)

            word_array = text.split()
            # other text normalization
            #punct = re.compile('[!,\.\?]')
            #word_array = [punct.sub(' ', word) for word in word_array]
            
            # basic spellcheck
            misspelled = spellcheck(word_array)
            # ignore words that are too short
            longenough = [word for word in misspelled if len(word) > 1]
            print('Misspelled: ', longenough)
            
            # check special cases
            # find doubled words and super long words
            repeated_words = find_repeated_words(word_array)
            print('Repeated words: ', repeated_words)
            # find words that are too long
            toolong = [word for word in word_array if len(word) > 15]
            print('Too Long: ', toolong)
            
            

exit()


