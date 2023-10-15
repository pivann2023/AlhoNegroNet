from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class dadosIOT(models.Model):
  lote_id     = models.IntegerField()
  hw_vers     = models.CharField(max_length=10)
  sw_vers     = models.CharField(max_length=10)
  set_point   = models.FloatField()
  temperatura = models.FloatField()
  humidade    = models.FloatField()
  data_hora   = models.DateTimeField()
  serialNumber= models.CharField(max_length=50,null=True)

class estufa(models.Model):
  nomeIOT    = models.CharField(max_length=10)
  senhaIOT   = models.CharField(max_length=20)
  capacidade = models.IntegerField() 
  user       = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT
  )
  STATUS_ESTUFA_CHOICES = [
    ('produzindo','produzindo'),
    ('erro','erro'),
    ('parada','parada')
  ]
  status     = models.CharField(
    max_length=20,
    choices=STATUS_ESTUFA_CHOICES,
    default='produzindo'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True,null=True
  )
  def __str__(self):
        return self.nomeIOT
  

class lote(models.Model):
  estufa = models.ForeignKey(
    'estufa',
    on_delete=models.PROTECT
  )
  peso_inicial = models.FloatField()
  peso_final   = models.FloatField(null=True)
  data_inicio  = models.DateTimeField()
  data_final   = models.DateTimeField(null=True)
  temperatura  = models.FloatField()
  STATUS_LOTE_CHOICES = [
    ('preparando','preparando'),
    ('iniciado','iniciado'),
    ('cancelado','cancelado'),
    ('finalizado','finalizado'),
    ('reservado','reservado'),
    ('vendido','vendido'),
  ]
  situacao = models.CharField(
    max_length=20,
    choices=STATUS_LOTE_CHOICES,
    default='preparando') 
  valor = models.FloatField(null=True)


class reserva(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT
  )
  lote = models.ForeignKey(
    'lote',
    on_delete=models.PROTECT
  )
  data_reserva = models.DateTimeField(auto_now_add=True)
  prepago = models.FloatField(default=0)


class compras(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT
  )
  lote = models.ForeignKey(
    'lote',
    on_delete=models.PROTECT
  )
  data_compra = models.DateTimeField(auto_now_add=True)
  valor = models.FloatField(default=0)
  status = models.CharField(max_length=20)

#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
