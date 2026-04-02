from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm
from django.views.generic import CreateView, TemplateView, UpdateView

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    #success_url = reverse_lazy('login')
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # автоматически входим после регистрации
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user