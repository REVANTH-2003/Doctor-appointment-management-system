from django.contrib import admin
from .models import User, Doctor,Patient,Blog


class DoctorAdmin(admin.ModelAdmin): 
    list_display=['first_name','last_name'] 

class PatientAdmin(admin.ModelAdmin): 
    list_display=['first_name','last_name'] 

class BlogAdmin(admin.ModelAdmin): 
    list_display=['user','title','category']

admin.site.register(User)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient,PatientAdmin)

