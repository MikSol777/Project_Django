from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import EmailAuthenticationForm, UserRegistrationForm


class UserRegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        messages.success(self.request, "Registration successful. Welcome!")
        return super().form_valid(form)

    def send_welcome_email(self, email):
        subject = "Welcome to our service"
        message = "Thank you for registering. We're glad to have you with us!"
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
        send_mail(subject, message, from_email, [email], fail_silently=True)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

