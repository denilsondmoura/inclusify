import requests
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
    LoginView as BaseLoginView,
)


class LoginView(BaseLoginView):

    template_name = 'registration/login.html'
    success_url = reverse_lazy('password_change_done')
    form_class = AuthenticationForm

    def form_valid(self, form):
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Redefinir senha'
        return context

    def get_success_url(self):
        return super().get_success_url()


class PasswordChangeView(LoginRequiredMixin, BasePasswordChangeView):

    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Redefinir senha'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Senha atualizada com sucesso!')
        return super().get_success_url()
    
