from django.shortcuts import render,HttpResponse

# Create your views here.
#### fazer isto: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import *
from .tokens import account_activation_token
from .models import *
from django.contrib.auth import login as contLogin, authenticate, logout as contLogout
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.encoding import force_str
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from pprint import pprint
from datetime import datetime
from datetime import date
from django.core.mail import EmailMessage
import os
from django.contrib import messages

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import io
import urllib.parse
import base64

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Ativação da conta Alho Net'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #user.email_user(subject, message)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message,to=[to_email])
            email.content_subtype="html"
            email.send()
            return account_activation_sent(request)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token): 
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        pprint(uid)
        pprint(user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        contLogin(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
    
    
def account_activation_sent(request) :
    return render(request,'account_activation_sent.html')    
    
#def home(request) :
#   return render(request,'home.html')    

def login(request) :  
    if request.method == 'GET':
      return render(request,'login.html',{'form':AuthenticationForm})    
    else :
      user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
      if user is not None:
          contLogin(request, user)
          return redirect('home')
      else:
        meuForm = AuthenticationForm(request.POST)
        meuForm.full_clean()
        meuForm.cleaned_data={}
        meuForm.add_error(error=['Credenciais inválidas ou e-mail não confirmado...'],field='username')
    
        return render(request,'login.html',{'form':meuForm})   
    
    
def logout(request):
  contLogout(request)
  return render(request,'home.html')

@login_required
def estufa_list(request):
    estufas = estufa.objects.all().filter(user=request.user)
    return render(request,"estufa/index.html",{'estufas':estufas})

@login_required
def estufa_view(request, pk):
    estufas = get_object_or_404(estufa, pk=pk)    
    return render(request, "estufa/view.html", {'object':estufas})

@login_required
def estufa_create(request, template_name='estufa/edit.html'):
    form = EstufaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('estufa_list')
    return render(request, template_name, {'form':form})

@login_required
def estufa_update(request, pk, template_name='estufa/edit.html'):
    estufas = get_object_or_404(estufa, pk=pk)
    form = EstufaForm(request.POST or None, instance=estufas)
    if form.is_valid():
        form.save()
        return redirect('estufa_list')
    return render(request, template_name, {'form':form})

@login_required
def estufa_delete(request, pk, template_name='estufa/delete.html'):
    estufas = get_object_or_404(estufa, pk=pk)    
    if request.method=='POST':
        try:
          estufas.delete()
          return redirect('estufa_list')
        except Exception as e:
          messages.error(request,'Ainda existem Lotes nessa Estufa. Remova os lotes primeiro.')
          return redirect('estufa_list')
    return render(request, template_name, {'object':estufas})


@login_required
def lote_list(request):
    estufas = estufa.objects.all().filter(user=request.user)
    lotes = lote.objects.all().filter(estufa__in=estufas)
    return render(request,"lote/index.html",{'lotes':lotes})

@login_required
def lote_view(request, pk):
    lotes = get_object_or_404(lote, pk=pk)    
    return render(request, "lote/view.html", {'object':lotes})

@login_required
def lote_create(request, fk=0, template_name='lote/edit.html'):
    pprint(request.POST)
    form = LoteForm(request.POST or None)
    pprint(form.data)
    if form.is_valid():
        pprint(form.cleaned_data)
        form.save()
        return redirect('lote_list')
    return render(request, template_name, {'form':form, 'estufa_id':fk})

@login_required
def lote_update(request, pk, template_name='lote/edit.html'):
    lotes = get_object_or_404(lote, pk=pk)
    form = LoteForm(request.POST or None, instance=lotes)
    if form.is_valid():
        form.save()
        return redirect('lote_list')
    return render(request, template_name, {'form':form,'estufa_id':lotes.estufa.id})

@login_required
def lote_delete(request, pk, template_name='lote/delete.html'):
    lotes = get_object_or_404(lote, pk=pk)    
    if request.method=='POST':
        try:
          lote.delete()
          return redirect('lote_list')
        except Exception as e:
          messages.error(request,'Ainda existem dados nesse Lote. Não é possível remover.')
          return redirect('lote_list')
    return render(request, template_name, {'object':lotes})

@login_required
def lote_iot_list(request, pk):
    iots = dadosIOT.objects.all().filter(lote_id=pk).order_by('data_hora')
    return render(request,"lote/iot.html",{'IOTs':iots,'lote_id':pk})

@login_required
def lote_iot_certificado(request,pk=0):
    df = pd.DataFrame(dadosIOT.objects.all().filter(lote_id=pk).values('data_hora','temperatura','set_point','humidade'))
    fig, ax = plt.subplots(figsize=(18,12.7))

    df.plot(kind='line',x='data_hora',y='temperatura',ax=ax,label='Temperatura')
    plt.ylabel('Temperatura',size=14)
    df.plot(kind='line',x='data_hora',y='set_point',ax=ax,label='Configuração')
    df.plot(kind='line',x='data_hora',y='humidade',ax=ax, label='Umidade',secondary_y=True)
    plt.ylabel('Umidade',size=14)
    plt.title('Certificado de produção do Lote - '+str(pk))
    fig.text(0.3,0.03,"Gerado por "+request.user.username+" em "+datetime.now().strftime("%d/%m/%Y %H:%M:%S"),size=12)
    ax.set_xlabel('Horários coletados',size=14)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    imgStr=base64.b64encode(buf.read())
    uriStr=urllib.parse.quote(imgStr)
    return render(request,'lote/certificate.html',{'data':uriStr, 'lote_id':pk})

@login_required
def reserva_list(request):
    reservas = reserva.objects.all().filter(user=request.user)
    return render(request,"reserva/index.html",{'reservas':reservas})

@login_required
class reservaView(DetailView):
    model = reserva