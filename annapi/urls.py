from django.urls import path
from . import views

urlpatterns= [
  path('data/<slug:deviceID>/',views.save_dadosIOT)
]