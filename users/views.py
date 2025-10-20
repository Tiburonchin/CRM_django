from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile


class SignUpView(CreateView):
    """
    HU 3: Vista de registro de usuario
    """
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return response


class CustomLoginView(LoginView):
    """
    HU 4: Vista de inicio de sesión personalizada
    """
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido, {form.get_user().username}!')
        return super().form_valid(form)


@login_required
def profile_view(request):
    """
    HU 5: Vista del perfil de usuario
    """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('users:profile')
    else:
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def home_view(request):
    """
    Vista principal del sistema
    """
    return render(request, 'home.html')
