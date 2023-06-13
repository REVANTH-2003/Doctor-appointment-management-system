from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.patient_home, name="patient-page"),
    path("doctor/", views.doctor_home, name="doctor-page"),
    path("draft/", views.draft, name="draft"),
    path("update-profile/", views.update_detail, name="update-profile"),
    path("doctor-profile/", views.doctor_profile , name="doctor-profile"),
    path("doctor-profile/<str:dusername>/", views.appointment , name="appointment-form"),
    path("appointment-notification/", views.appnotify , name="appointment-notification"),
    path("appointment-notification/<str:pusername>/<str:date>/", views.confirm , name="appointment-confirm"),
    path("confirmed-appointment/", views.appconfirm , name="confirmed-appointment"),
    path("docter/calender/", views.calender , name="calender"),

    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/patient/", views.PatientSignUpView.as_view(), name="patient-signup"),
    path("signup/doctor/", views.DoctorSignUpView.as_view(), name="doctor-signup"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]