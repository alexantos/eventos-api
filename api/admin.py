from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from api.models import Evento, EventoSympla, Integracao

admin.site.register(Evento, SimpleHistoryAdmin)
admin.site.register(EventoSympla, SimpleHistoryAdmin)

admin.site.register(Integracao)