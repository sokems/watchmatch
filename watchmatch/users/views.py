from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .forms import CustomUserCreationForm, GetTokenForm


class CreateUserView(CreateView):
    """Вьюха для регистрации"""
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.save()
        login(self.request, user)

        return response


class GetTokenView(FormView):
    """Вьюха для получения API токена"""
    template_name = 'users/get_token.html'
    form_class = GetTokenForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            form.add_error(None, 'Неверный логин или пароль')
            return self.form_invalid(form)

        token, created = Token.objects.get_or_create(user=user)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                token=token.key
            )
        )
