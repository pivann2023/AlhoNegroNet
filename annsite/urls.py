from django.urls import path, re_path, include
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth.models import User
from django.contrib.auth.views import *
from django.contrib.auth.urls import urlpatterns as authUrlsPatterns


urlpatterns = [
    path('',TemplateView.as_view(template_name='home.html'),name='home'),
    path('login/',login,name='login'),
    path('accounts/login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('signup',signup,name='signup'),
    path('account_activation_sent', account_activation_sent, name='account_activation_sent'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    path('ajuda',TemplateView.as_view(template_name='ajuda.html'),name='ajuda'),
    path('estufas',estufa_list,name='estufa_list'),
    path('estufas/<int:pk>',estufa_view,name='estufa_view'),
    path('estufas/new', estufa_create, name='estufa_new'),
    path('estufas/edit/<int:pk>', estufa_update, name='estufa_edit'),
    path('estufas/delete/<int:pk>', estufa_delete, name='estufa_delete'),
    path('lotes',lote_list,name='lote_list'),
    path('lotes/<int:pk>',lote_view,name='lote_view'),
    path('lotes/new/<int:fk>',lote_create,name='lote_new'),
    path('lotes/edit/<int:pk>', lote_update, name='lote_edit'),
    path('lotes/delete/<int:pk>', lote_delete, name='lote_delete'),
    path('lotes/iot/<int:pk>', lote_iot_list, name='lote_iot_list'),
    path('lotes/iot/certificado/<int:pk>',lote_iot_certificado,name='lote_iot_certificado'),
    path('reservas',reserva_list,name='reserva_list'),
    path('reservas/<int:pk>',reservaView,name='reserva_view')
    
]

urlpatterns = urlpatterns + authUrlsPatterns