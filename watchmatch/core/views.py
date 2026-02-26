from django.shortcuts import render


def index(request):
    """Главная страница"""
    template_name = 'core/index.html'
    return render(request, template_name)


def about(request):
    """Страница о проекте"""
    template_name = 'core/about.html'
    return render(request, template_name)


def page_not_found(request, exception):
    """Страница не найдена"""
    return render(request, 'core/404.html', status=404)


def csrf_failure(request, reason=''):
    """Ошибка csrf токена"""
    return render(request, 'core/403csrf.html', status=403)


def bad_request(request, exception):
    """Ошибка запроса"""
    return render(request, 'core/400.html', status=400)


def server_error(request):
    """Ошибка сервера"""
    return render(request, 'core/500.html', status=500)
