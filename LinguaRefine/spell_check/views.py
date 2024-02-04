from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'spell_check/index.html') # This line returns the index.html template

def spell_check(request):
    pass
    
def grammar_check(request):
    pass
 