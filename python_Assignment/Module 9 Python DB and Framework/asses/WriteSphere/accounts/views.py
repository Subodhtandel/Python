from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView

from .forms import ProfileForm, RegistrationForm
from .models import User


class RegistrationView(FormView):
    template_name = "registration/signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Welcome to WriteSphere.")
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, "Profile updated.")
        return reverse_lazy(
            "blog:author_profile",
            kwargs={"username": self.request.user.username},
        )
