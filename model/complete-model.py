import nltk
from nltk.corpus import wordnet
import string
from textblob import TextBlob
from happytransformer import HappyTextToText, TTSettings
# nltk.download('punkt')
# nltk.download('wordnet')

from nltk.tokenize import sent_tokenize, word_tokenize

sentence = "Hello, my naame a John. I am a software develoer. I am learning NLP."

sentence_without_punctuation = sentence.translate(str.maketrans('', '', string.punctuation))

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


print(words_not_found)

print(sentence)
print (corrections)

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)
result = happy_tt.generate_text("grammar: " + sentence, args=args)
print(result.text)
