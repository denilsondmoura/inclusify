from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import ProfileCreationForm
from .models import Profile


class AccountLoginView(LoginView):

    template_name = 'registration/account_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('postagens_relevantes_list')
    
class AccountRegisterView(CreateView):
    model = Profile
    form_class = ProfileCreationForm
    template_name = "registration/account_register.html"
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastrar-se'
        return context

    def get_success_url(self):
        return reverse_lazy('accounts:login')
    
class AccountPasswordResetView(PasswordResetView):
    template_name = "registration/account_password_reset_form.html"
    email_template_name = "registration/account_password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")

class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/account_password_reset_done.html"

class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/account_password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/account_password_reset_complete.html"
    
class AccountProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Perfil'
        context["user"] = self.request.user
        return context
    
class AccountProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile_edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Editar Perfil'
        context["user"] = self.request.user
        return context
    
def account_logout(request):
    logout(request)
    return redirect("accounts:login")
