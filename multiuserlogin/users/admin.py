from django.contrib import admin
from .models import User, Doctor,Patient


class DoctorAdmin(admin.ModelAdmin): 
    list_display=['first_name','last_name'] 

class PatientAdmin(admin.ModelAdmin): 
    list_display=['first_name','last_name'] 

admin.site.register(User)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient,PatientAdmin)

