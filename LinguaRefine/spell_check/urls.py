from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('grammar_check/', views.grammar_check, name='grammar_check'),
]