from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User,Blog,Doctor,Patient,AppointmentDetail
from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm, BlogPostForm,UpdateForm,AppointmentForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import patient_required, doctor_required
import os
import pickle
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = './templates/users/client_id.json'
TOKEN_FILE = 'token.pickle'


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
    option1 = Blog.objects.filter(status='post',category = "Mental Health")
    option2 = Blog.objects.filter(status='post',category = "Heart Disease")
    option3 = Blog.objects.filter(status='post',category = "Covid19")
    option4 = Blog.objects.filter(status='post',category = "Immunization")
    return render(request, 'users/patient_home.html',{'mental':option1,'heart':option2,'covid':option3,'immunization':option4,'user':request.user})

@login_required
@doctor_required
def doctor_home(request):
    forms = BlogPostForm()
    option1 = Blog.objects.filter(status='post',category = "Mental Health")
    option2 = Blog.objects.filter(status='post',category = "Heart Disease")
    option3 = Blog.objects.filter(status='post',category = "Covid19")
    option4 = Blog.objects.filter(status='post',category = "Immunization")

    if request.method == 'POST': 
        form = BlogPostForm(request.POST, request.FILES) 
        if form.is_valid():
            user = request.user
            blog = Blog()  
            blog.title = form.cleaned_data['title']
            blog.category = form.cleaned_data['category']
            blog.summary = form.cleaned_data['summary']
            blog.content = form.cleaned_data['content']
            blog.image = form.cleaned_data['image']
            blog.status = form.cleaned_data['status']
            blog.user = user.username
            blog.save()
            render(request, 'users/doctor_home.html', {'form': forms,'mental':option1,'heart':option2,'covid':option3,'immunization':option4,'user':request.user})
    return render(request, 'users/doctor_home.html', {'form': forms,'mental':option1,'heart':option2,'covid':option3,'immunization':option4,'user':request.user})

@login_required
@doctor_required
def draft(request):
    forms = BlogPostForm()
    draft = Blog.objects.filter(status='draft',)
    return render(request, 'users/draft.html', {'draft':draft,'user':request.user,'form':forms})


@login_required
def update_detail(request):
    user = request.user
    if user.is_doctor:
        forms = UpdateForm(initial={'first_name':user.doctor.first_name,'last_name':user.doctor.last_name,'email':user.email,'address':user.doctor.address,'profile':user.doctor.profile})
    elif user.is_patient:
        forms = UpdateForm(initial={'first_name':user.patient.first_name,'last_name':user.patient.last_name,'email':user.email,'address':user.patient.address,'profile':user.patient.profile})

    if request.method == 'POST': 
        form = UpdateForm(request.POST, request.FILES) 
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
        if user.is_doctor:
            doc_obj = Doctor.objects.get(user=user)
            doc_obj.first_name = form.cleaned_data['first_name']
            doc_obj.last_name = form.cleaned_data['last_name']
            doc_obj.email = form.cleaned_data['email']
            doc_obj.profile = form.cleaned_data['profile']
            doc_obj.address = form.cleaned_data['address']
            doc_obj.save()
            return redirect('doctor-page')
        elif user.is_patient:
            pat_obj = Patient.objects.get(user=user)
            pat_obj.first_name = form.cleaned_data['first_name']
            pat_obj.last_name = form.cleaned_data['last_name']
            pat_obj.email = form.cleaned_data['email']
            pat_obj.profile = form.cleaned_data['profile']
            pat_obj.address = form.cleaned_data['address']
            pat_obj.save()
            return redirect('patient-page')

    return render(request, 'users/updatedetails.html', {'user':request.user,'form':forms})


@login_required
@patient_required
def doctor_profile(request):
    doctors = User.objects.filter(is_doctor = True)
    return render(request, 'users/doctors_details.html', {'doctor':doctors} )


@login_required
@patient_required
def appointment(request,dusername):
    forms = AppointmentForm(initial={'doctor_username':dusername,})
    forms.doctor_username = dusername

    if request.method == 'POST': 
        form = AppointmentForm(request.POST, request.FILES) 
        if form.is_valid():
            user = request.user
            entry = AppointmentDetail()  
            entry.doctor_username = dusername
            entry.patient_username = user.username
            entry.required_speciality = form.cleaned_data['speciality']
            entry.appointmentDate = form.cleaned_data['appointmantDate']

            dt_str = form.cleaned_data['appointmantDate'].strftime("%Y-%m-%d")

            date_obj = datetime.strptime(dt_str, '%Y-%m-%d')
            new_date_string = date_obj.strftime('%Y-%m-%d')

            entry.start_time = form.cleaned_data['startTime']

            time_obj = datetime.strptime( new_date_string +" "+ form.cleaned_data['startTime'].strftime("%H:%M"), "%Y-%m-%d %H:%M")
            new_time_obj = time_obj + timedelta(minutes=45)
            new_time = new_time_obj.strftime("%H:%M")
            entry.end_time = new_time
            entry.appointmantStatus= False
            entry.save()
            return redirect('doctor-profile')
        
    return render(request, 'users/appointmentform.html', {'form': forms})


@login_required
@doctor_required
def appnotify(request):
    datas = AppointmentDetail.objects.filter(doctor_username = request.user.username, appointmentStatus = False)
    return render(request, 'users/doctor_confirmation.html', {'data': datas,})


@login_required
@doctor_required
def confirm(request,pusername,date):
    datas = AppointmentDetail.objects.get(patient_username = pusername, appointmentDate=date, appointmentStatus=False)
    datas.appointmentStatus = True
    datas.save()

    def get_credentials():
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow.run_local_server(port=0)
                credentials = flow.credentials
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        return credentials
    
    
    credentials = get_credentials()
    service = build('calendar', 'v3', credentials=credentials)

    datetime_obj1 = datetime.combine(datas.appointmentDate, datas.start_time)
    datetime_obj2= datetime.combine(datas.appointmentDate, datas.end_time)
    

    event = {
            'summary': 'Appoinment Event',
            'location': 'Theni, Tamil Nadu, India',
            'description': datas.required_speciality,
            'start': {
                'dateTime': datetime_obj1.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': datetime_obj2.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': True,
            },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

    return redirect('appointment-notification')


@login_required
@patient_required
def appconfirm(request):
    datas = AppointmentDetail.objects.filter(patient_username = request.user.username, appointmentStatus = True)
    data1 = AppointmentDetail.objects.filter(patient_username = request.user.username, appointmentStatus = False)
    return render(request, 'users/confirmed_appointment.html', {'data': datas,'data1':data1} )


@login_required
@doctor_required
def calender(request):
    return render(request, 'users/calender.html')
