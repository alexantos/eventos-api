from telnetlib import STATUS

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Evento, IntegracaoSympla, EventoSympla
from api.serializers import EventoSerializer, IntegracaoSymplaSerializer, EventoSymplaSerializer


class EventoView(viewsets.ModelViewSet):
    queryset = Evento.objects.filter().order_by('-criacao')
    serializer_class = EventoSerializer
    # permission_classes = [permissions.IsAuthenticated]


class IntegracaoSymplaView(viewsets.ModelViewSet):
    queryset = IntegracaoSympla.objects.filter().order_by('-criacao')
    serializer_class = IntegracaoSymplaSerializer
    # permission_classes = [permissions.IsAuthenticated]


class EventoSymplaView(viewsets.ModelViewSet):
    queryset = EventoSympla.objects.filter().order_by('-criacao')
    serializer_class = EventoSymplaSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def atualiza_eventos_sympla(request):
    try:
        import requests
        headers = {
            's_token': '0fac2f20a2fd038e75667efc027bd68e3f1ce91ce693d7c20eeaf38f53c5fdab'
        }
        result = requests.get(url='https://api.sympla.com.br/public/v1.5.1/events?sort=DESC', headers=headers)
        response = result.json()
        integracao = IntegracaoSympla.objects.create(requisicao=response, status_code=result.status_code)

        for event in response['data']:
            if not EventoSympla.objects.filter(id_sympla=event['id']).exists():
                evento = Evento.objects.create(
                    nome=event['name'],
                    data_hora_inicio=event['start_date'],
                    data_hora_fim=event['end_date'],
                    categoria=event['category_prim'],
                )
                EventoSympla.objects.create(
                    id_sympla=event['id'],
                    reference_id=event['reference_id'],
                    evento=evento,
                    integracao=integracao
                )
            else:
                evento_sympla_salvo = EventoSympla.objects.filter(id_sympla=event['id']).first()
                evento_salvo = Evento.objects.filter(id=evento_sympla_salvo.evento.id)
                evento_salvo.update(
                    nome=event['name'],
                    data_hora_inicio=event['start_date'],
                    data_hora_fim=event['end_date'],
                    categoria=event['category_prim'],
                )
        return Response('Atualizado os eventos com sucesso!', status=status.HTTP_200_OK)

    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return Response('Ocorreu um erro inesperado', status=status.HTTP_400_BAD_REQUEST)
