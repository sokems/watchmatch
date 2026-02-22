from django.shortcuts import render


def index(request):
    """Главная страница"""
    template_name = 'core/index.html'
    return render(request, template_name)


def about(request):
    """Страница о проекте"""
    template_name = 'core/about.html'
    return render(request, template_name)
