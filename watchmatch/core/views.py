from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    """Главная страница"""
    template_name = 'core/index.html'
    return render(request, template_name)


def about(request):
    """Станица о проекте"""
    return HttpResponse('О проекте')
