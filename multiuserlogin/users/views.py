from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User,Blog,Doctor,Patient
from .forms import DoctorSignUpForm, PatientSignUpForm, LoginForm, BlogPostForm,UpdateForm
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



