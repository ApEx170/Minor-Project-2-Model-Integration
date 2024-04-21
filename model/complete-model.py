import nltk
from nltk.corpus import wordnet
import string
from textblob import TextBlob
from happytransformer import HappyTextToText, TTSettings

# nltk.download('punkt')
# nltk.download('wordnet')

from nltk.tokenize import sent_tokenize, word_tokenize

sentence = "Hello, my naame a John. I am a software develoer. I am learning NLP."

sentence_without_punctuation = sentence.translate(
    str.maketrans("", "", string.punctuation)
)

words = word_tokenize(sentence_without_punctuation)
# sent = sent_tokenize(sentence)

words_not_found = []

for word in words:
    # print(word)
    if not wordnet.synsets(word):
        words_not_found.append(word)

corrections = {}

for word in words_not_found:
    corrected_word = str(TextBlob(word).correct())
    sentence = sentence.replace(word, corrected_word)
    corrections[word] = corrected_word

import string
import re
import numpy as np
from collections import Counter
from pathlib import Path


# importing data
def read_corpus(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

        words = []
        for word in lines:
            words += re.findall(r"\w+", word.lower())
    return words


def update_vocab(corpus):
    return set(corpus)


ROOT_DIR = Path(__file__).parent
psub_file = ROOT_DIR / "big_corpus.txt"

# invoke this function
corpus = read_corpus(psub_file)
vocab = update_vocab(corpus)
words_count = Counter(corpus)
total_words_count = float(sum(words_count.values()))
word_probabs = {
    word: words_count[word] / total_words_count for word in words_count.keys()
}


def split(word):  # why
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def delete(word):
    return [left + right[1:] for left, right in split(word) if right]


def swap(word):
    return [
        left + right[1] + right[0] + right[2:]
        for left, right in split(word)
        if len(right) > 1
    ]


def replace(word):  # abcdef...z
    return [
        left + center + right[1:]
        for left, right in split(word)
        if right
        for center in string.ascii_lowercase
    ]


def insert(word):  # abcdef...z
    return [
        left + center + right[1:]
        for left, right in split(word)
        for center in string.ascii_lowercase
    ]


def level_one_edits(word):
    return set((delete(word) + swap(word) + replace(word) + insert(word)))


def level_two_edits(word):
    return set(e2 for e1 in level_one_edits(word) for e2 in level_one_edits(e1))


def check_correct_spelling(words_not_found, vocab, word_probabs):
    correct_list = {}
    for word in words_not_found:

        if word in vocab:
            continue
        # getting all suggesions
        suggestions = level_one_edits(word) or level_two_edits(word) or [word]
        best_guesses = [w for w in suggestions if w in vocab]
        if not best_guesses:
            correct_list[word] = 0
        suggestions_with_probabs = [w for w in best_guesses]
        suggestions_with_probabs.sort(key=lambda x: x[1], reverse=True)
        correct_list[word] = suggestions_with_probabs
    return correct_list


print(words_not_found)
print(sentence)
print(corrections)
print(check_correct_spelling(words_not_found, vocab, word_probabs))

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)
result = happy_tt.generate_text("grammar: " + sentence, args=args)
print(result.text)
