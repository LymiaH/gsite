from django.urls import path, re_path
from gradio import views

app_name = 'gradio'

urlpatterns = [
    path('', views.latest, name='latest'),
    re_path(r'^smtv/(?P<path>.+)$', views.smtv, name='smtv')
]
