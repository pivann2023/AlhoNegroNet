from django.contrib import admin
from .models import *

# Register your models here.
class LoteInline(admin.TabularInline):
   model = lote

class estufaAdmin(admin.ModelAdmin):
    fields =['nomeIOT','senhaIOT','capacidade','user','status','created_at']
    list_display = ('nomeIOT','senhaIOT','capacidade','user','status','created_at','modified_at')
    createonly_fields = ['nomeIOT','senhaIOT','capacidade','user','created_at' ]
    ordering = ['nomeIOT','user','modified_at']
    inlines = [LoteInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(estufaAdmin, self).get_readonly_fields(request, obj))
        createonly_fields = list(getattr(self, 'createonly_fields', ['created_at','modified_at']))   
        if obj:  # editing an existing object
            readonly_fields.extend(createonly_fields)
        return readonly_fields
  
admin.site.register(estufa,estufaAdmin)

class loteAdmin(admin.ModelAdmin):
  fields =['id','estufa','peso_inicial','peso_final','data_inicio','data_final','temperatura','situacao','valor']
  list_display = ('id','estufa','peso_inicial','peso_final','data_inicio','data_final','temperatura','situacao','valor')
  createonly_fields = ['id','estufa','peso_inicial','peso_final','data_inicio','data_final','temperatura','situacao','valor' ]
  ordering = ['estufa','id']

  def get_readonly_fields(self, request, obj=None):
    readonly_fields = list(super(estufaAdmin, self).get_readonly_fields(request, obj))
    createonly_fields = list(getattr(self, 'createonly_fields', []))   
    if obj:  # editing an existing object
        readonly_fields.extend(createonly_fields)
    return readonly_fields

admin.site.register(lote,loteAdmin)

class reservaAdmin(admin.ModelAdmin):
  pass

admin.site.register(reserva,reservaAdmin)

class comprasAdmin(admin.ModelAdmin):
  pass

admin.site.register(compras,comprasAdmin)

class dadosIOTAdmin(admin.ModelAdmin): 
  fields =['lote_id','hw_vers','sw_vers','set_point','tmperatura','humidade','data_hora','serialNumber']
  list_display = ('lote_id','hw_vers','sw_vers','set_point','temperatura','humidade','data_hora','serialNumber')
  createonly_fields = ['lote_id','hw_vers','sw_vers','set_point','temperatura','humidade','data_hora','serialNumber' ]
  ordering = ['lote_id','data_hora']

  def get_readonly_fields(self, request, obj=None):
    readonly_fields = list(super(estufaAdmin, self).get_readonly_fields(request, obj))
    createonly_fields = list(getattr(self, 'createonly_fields', []))   
    if obj:  # editing an existing object
      readonly_fields.extend(createonly_fields)
    return readonly_fields

admin.site.register(dadosIOT,dadosIOTAdmin)
