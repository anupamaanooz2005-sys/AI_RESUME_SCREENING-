from django.urls import path
from . import views

urlpatterns = [
    path('',            views.home,         name='home'),
    path('candidate/',  views.candidate,    name='candidate'),
    path('hr/',         views.hr_dashboard, name='hr'),
    path('hr/analyze/', views.hr_analyze,   name='hr_analyze'),
    path('share/',      views.share,        name='share'),
]
