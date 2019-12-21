from django.urls import path

from gradio import views

app_name = 'gradio'

urlpatterns = [
    path('', views.latest, name='latest'),
]
