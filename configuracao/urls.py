from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import EventoView, atualiza_eventos_sympla

router = routers.DefaultRouter()
router.register(r'evento', EventoView)

urlpatterns = [
    path('', include(router.urls)),


    path('atualiza-eventos-sympla', atualiza_eventos_sympla),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
