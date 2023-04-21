from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Doctor, Patient
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

