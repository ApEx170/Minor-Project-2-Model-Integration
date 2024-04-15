# views.py

import json

from django.shortcuts import render
from django.http import JsonResponse
from happytransformer import HappyTextToText, TTSettings

def index(request):
    return render(request, 'spell_check/index.html')

def grammar_check(request):
    if request.method == 'POST':
 
        data = json.loads(request.body)
        input_text = data.get('input_text', '')

        happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
        args = TTSettings(num_beams=5, min_length=1)
        result = happy_tt.generate_text("grammar: " + input_text, args=args)

        return JsonResponse({'corrected_text': result.text})

    # Return error for unsupported HTTP methods
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
