from django.contrib import admin
from feedbackForm.models import RatingQuestion, Users, Feedbacks, Professors, Courses
import django.contrib.auth.models

# Register your models here.
admin.site.register(RatingQuestion)
admin.site.register(Users)
admin.site.register(Feedbacks)
admin.site.register(Professors)
admin.site.register(Courses)
#admin.site.register(django.contrib.auth.models.User)
