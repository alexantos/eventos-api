from api.models import EventoSympla, Evento, Integracao
import requests

from configuracao.settings import SYMPLA_TOKEN


def integracao_sympla(request):
    try:
        headers = {
            's_token': SYMPLA_TOKEN
        }
        result = requests.get(url='https://api.sympla.com.br/public/v1.5.1/events?sort=DESC', headers=headers)
        response = result.json()
        integracao = Integracao.objects.create(requisicao=response, status_code=result.status_code,
                                               api_consulta='SYMPLA')

        for event in response['data']:
            if not EventoSympla.objects.filter(id_sympla=event['id']).exists():
                evento = Evento.objects.create(
                    nome=event['name'],
                    data_hora_inicio=event['start_date'],
                    data_hora_fim=event['end_date'],
                    categoria=event['category_prim']['name'],
                )
                EventoSympla.objects.create(
                    id_sympla=event['id'],
                    reference_id=event['reference_id'],
                    evento=evento,
                    integracao_sympla=integracao,
                )
            else:
                evento_sympla_salvo = EventoSympla.objects.filter(id_sympla=event['id']).first()
                evento_sympla_salvo.integracao_sympla = integracao
                evento_sympla_salvo.save()

                evento_salvo = Evento.objects.get(id=evento_sympla_salvo.evento.id)
                evento_salvo.nome = event['name']
                evento_salvo.data_hora_inicio = event['start_date']
                evento_salvo.data_hora_fim = event['end_date']
                evento_salvo.categoria = event['category_prim']['name']
                evento_salvo.save()

        return 'Atualizado os eventos com sucesso!'

    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return "Ocorreu um erro inesperado"
