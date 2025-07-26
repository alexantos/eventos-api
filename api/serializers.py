from rest_framework import serializers

from api.models import Evento, EventoSympla


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class EventoSymplaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoSympla
        fields = '__all__'
