import uuid

from django.db import models


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

    def __str__(self):
        return self.nome


class IntegracaoSympla(ModelBase):
    requisicao = models.JSONField()
    status_code = models.CharField(max_length=4)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Integrações Sympla'


class EventoSympla(ModelBase):
    id_sympla = models.CharField(max_length=7)
    reference_id = models.CharField(max_length=7)
    evento = models.ForeignKey(to=Evento, on_delete=models.PROTECT)
    integracao = models.ForeignKey(to=IntegracaoSympla, on_delete=models.PROTECT)

    def __str__(self):
        return self.id_sympla

    class Meta:
        verbose_name_plural = 'Eventos Sympla'
