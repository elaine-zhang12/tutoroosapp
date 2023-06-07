from django.contrib import admin

# Register your models here.
from .models import*

admin.site.register(Course)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Request)
admin.site.register(Review)