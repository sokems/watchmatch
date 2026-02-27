from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login


class CreateUserView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.save()
        login(self.request, user)

        return response