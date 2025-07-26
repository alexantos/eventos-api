from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Evento, EventoSympla
from api.serializers import EventoSerializer, EventoSymplaSerializer


class EventoView(viewsets.ModelViewSet):
    queryset = Evento.objects.filter().order_by('-criacao')
    serializer_class = EventoSerializer

    @action(detail=False, methods=['get'], url_path='atualiza-eventos-sympla')
    def atualiza_eventos_sympla(self, request, pk=None):
        from api.integracoes.sympla import integracao_sympla
        try:
            integracao_sympla = integracao_sympla(request)
            return Response(integracao_sympla, status=status.HTTP_200_OK)
        except Exception as e:
            print("Ocorreu um erro inesperado: ", e)
            return Response('Ocorreu um erro inesperado', status=status.HTTP_400_BAD_REQUEST)


class EventoSymplaView(viewsets.ModelViewSet):
    queryset = EventoSympla.objects.filter().order_by('-criacao')
    serializer_class = EventoSymplaSerializer
