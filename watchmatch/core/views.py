import logging

from django.shortcuts import render


logger = logging.getLogger(__name__)


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
    logger.warning(f"404: {request.path}")
    return render(request, 'core/404.html', status=404)


def csrf_failure(request, reason=''):
    """Ошибка csrf токена"""
    logger.warning(f"CSRF failure: {reason}")
    return render(request, 'core/403csrf.html', status=403)


def bad_request(request, exception):
    """Ошибка запроса"""
    logger.warning(f"400 Bad Request: {request.path}")
    return render(request, 'core/400.html', status=400)


def server_error(request):
    """Ошибка сервера"""
    logger.error("500 Server Error")
    return render(request, 'core/500.html', status=500)
