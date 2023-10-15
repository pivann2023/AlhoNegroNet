from rest_framework import serializers
from annsite.models import *

class dadosIOTSerializer(serializers.ModelSerializer):
    class Meta:
      model = dadosIOT
      fields = ['lote_id' ,'hw_vers' ,'sw_vers' , 'set_point' ,'temperatura' ,'humidade' , 'data_hora' ,'serialNumber']
      #exclude = ['APIKEY']