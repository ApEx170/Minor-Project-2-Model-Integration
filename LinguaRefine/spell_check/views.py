from django.shortcuts import render
from django.http import JsonResponse
from happytransformer import HappyTextToText, TTSettings
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import string
from textblob import TextBlob
import nltk
import json

def index(request):
    return render(request, 'spell_check/index.html')

def grammar_check(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        input_text = data.get('input_text', '')
        
        words = word_tokenize(input_text.translate(str.maketrans('', '', string.punctuation)))
       
        words_not_found = [word for word in words if not wordnet.synsets(word)]
        
        corrections = {}
        for word in words_not_found:
            corrected_word = str(TextBlob(word).correct())
            input_text = input_text.replace(word, corrected_word)
            corrections[word] = corrected_word
        
        print(corrections)  
        
        happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
        args = TTSettings(num_beams=5, min_length=1)
        result = happy_tt.generate_text("grammar: " + input_text, args=args)
        
        return JsonResponse({'corrected_text': result.text, 'corrections': corrections})

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
