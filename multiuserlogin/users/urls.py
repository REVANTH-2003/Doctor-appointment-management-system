from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.patient_home, name="patient-page"),
    path("doctor/", views.doctor_home, name="doctor-page"),
    path("draft/", views.draft, name="draft"),
    path("update-profile/", views.update_detail, name="update-profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/patient/", views.PatientSignUpView.as_view(), name="patient-signup"),
    path("signup/doctor/", views.DoctorSignUpView.as_view(), name="doctor-signup"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]