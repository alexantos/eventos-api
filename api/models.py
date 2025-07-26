import uuid

from django.db import models
from simple_history.models import HistoricalRecords


class ModelBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Evento(ModelBase):
    nome = models.CharField(max_length=256)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    categoria = models.CharField(max_length=64)

    historico = HistoricalRecords()

    def __str__(self):
        return self.nome


API_CONSULTA = [
    ("SYMPLA", "Sympla"),
]


class Integracao(ModelBase):
    requisicao = models.JSONField()
    status_code = models.CharField(max_length=4)
    api_consulta = models.CharField(max_length=32, choices=API_CONSULTA)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Integrações'


class EventoSympla(ModelBase):
    id_sympla = models.CharField(max_length=7)
    reference_id = models.CharField(max_length=7)
    evento = models.ForeignKey(to=Evento, on_delete=models.PROTECT)
    integracao_sympla = models.ForeignKey(to=Integracao, on_delete=models.PROTECT)

    historico = HistoricalRecords()

    def __str__(self):
        return self.evento.nome

    class Meta:
        verbose_name_plural = 'Eventos Sympla'
