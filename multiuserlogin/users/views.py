from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User 
from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import patient_required, doctor_required


class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'users/patient_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patient-page')

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'users/doctor_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('doctor-page')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_patient:
                return reverse('patient-page')
            elif user.is_doctor:
                return reverse('doctor-page')
        else:
            return reverse('login')


@login_required
@patient_required
def patient_home(request):
    user = request.user
    return render(request, 'users/patient_home.html',{'user': user})

@login_required
@doctor_required
def doctor_home(request):
    return render(request, 'users/doctor_home.html')

