from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from annsite.models import *
from .serializers import *
from pprint import pprint

@api_view(['POST'])
def save_dadosIOT(request,deviceID):
  
  #pprint(serializer)
  # verificar tabela estufa nomeIOT x deviceID
  # senhaIOT x request.data request.data['teste']
  senha = request.data['APIKEY']
  dadosEstufa = estufa.objects.all().filter(nomeIOT=deviceID,senhaIOT=senha) # a estufa está cadastrada ?
  #pprint(dadosEstufa.values())
  if (dadosEstufa.count() == 1):
    dadosLote = lote.objects.all().filter(estufa_id=dadosEstufa.first().id,id=request.data['lote_id']) # lote está cadastrado e com status produzindo ?
    #pprint (dadosLote.values())
    if (dadosLote.count() == 1):
      if (dadosLote.first().situacao == 'produzindo'):
        #salvar registro
        serializer = dadosIOTSerializer(data=request.data)
        serializer.is_valid()
        #pprint(serializer)
        serializer.save()
        #print(str(dadosLote.first().id))
        return Response("Dados do Lote " + str(dadosLote.first().id) + " registrados.",status=status.HTTP_201_CREATED)
      else:
        #print('Nao produzindo -->'+dadosLote.first().situacao+'<--')
        return Response("Lote nao está com status 'produzindo'",status=status.HTTP_412_PRECONDITION_FAILED)
    else:
      #print('cadastro zoado')
      return Response("Cadastro do lote com problema",status=status.HTTP_417_EXPECTATION_FAILED)
  else:
    #Senha Inválida
    return Response("Estufa Não Cadastrada",status=status.HTTP_401_UNAUTHORIZED)



