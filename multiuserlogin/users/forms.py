from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Doctor, Patient,Blog
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientSignUpForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Enter First name",'id':'fname','required':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Enter Last name",'id':'lname'}))
    profile = forms.ImageField()
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Address:(city,address,pincode)",'id':'address','required':'required'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username','required':'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email','required':'required'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'aria-describedby':"emailHelp",'required':'required'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again','required':'required'}),
        }
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        patient = Patient.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), profile = self.cleaned_data['profile'], address =self.cleaned_data.get('address') )
        return user
    
class DoctorSignUpForm(UserCreationForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Enter First name",'id':'fname','required':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Enter Last name",'id':'lname'}))
    profile = forms.ImageField()
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Address:(city,address,pincode)",'id':'address','required':'required'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username','required':'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email','required':'required'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'aria-describedby':"emailHelp",'required':'required'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again','required':'required'}),
        }
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        doctor = Doctor.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), profile = self.cleaned_data['profile'], address =self.cleaned_data.get('address'))
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','aria-describedby':"emailHelp", 'placeholder' : "User Name",'id':'Username'},))
    password = forms.CharField(widget=forms.PasswordInput( attrs = {'class':"form-control" ,'id':"password",'placeholder':"password"}))


class UpdateForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'fname','required':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'lname','required':'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','required':'required','id':'mail'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'address','required':'required'}))
    profile = forms.ImageField()
    

class BlogPostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'title','required':'required'}))
    category = forms.ChoiceField(widget=forms.RadioSelect(attrs={'required':'required',}), choices=(('Mental Health','Mental Health'),('Heart Disease','Heart Disease'),('Covid19','Covid19'),('Immunization','Immunization')))
    summary = forms.CharField(widget=forms.Textarea(attrs={'id':'summary','cols':'50',"class":"form-control",'style':"height:70px"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'id':'content','cols':'50',"class":"form-control",'style':"height:70px"}))
    image = forms.ImageField()
    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={}), choices=(('post','Post'),('draft','Draft')))


class BlogPostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'title','required':'required'}))
    category = forms.ChoiceField(widget=forms.RadioSelect(attrs={'required':'required',}), choices=(('Mental Health','Mental Health'),('Heart Disease','Heart Disease'),('Covid19','Covid19'),('Immunization','Immunization')))
    summary = forms.CharField(widget=forms.Textarea(attrs={'id':'summary','cols':'50',"class":"form-control",'style':"height:70px"}))
    content = forms.CharField(widget=forms.Textarea(attrs={'id':'content','cols':'50',"class":"form-control",'style':"height:70px"}))
    image = forms.ImageField()
    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={}), choices=(('post','Post'),('draft','Draft')))

class AppointmentForm(forms.Form):
    doctor_username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'username','required':'required'}))
    speciality = forms.CharField(widget=forms.TextInput(attrs={'id':'speciality','required':'required','class':"form-control"}))
    appointmantDate = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','id':'date','type':'date', 'format':"yyyy-mm-dd"})) 
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','id':'time','type':'time'}))