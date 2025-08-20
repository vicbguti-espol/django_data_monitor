from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from datetime import datetime, timezone
import json

@login_required
def index(request):
    response = requests.get(settings.API_URL)  # URL de la API
    posts = response.json()  # Convertir la respuesta a JSON

    # Número total de respuestas
    total_responses = len(posts)

    conteo_por_tipo = {}
    for key, item in posts.items():
        tipo = item.get("tipo")  # Usa .get() para evitar errores si 'tipo' no existe
        if tipo:  # Asegura que 'tipo' no sea None
            conteo_por_tipo[tipo] = conteo_por_tipo.get(tipo, 0) + 1

    # Preparamos los datos para el gráfico
    chart_config = chart_data(posts)

    data = {
        "title": "Landing Page' Dashboard",
        "total_responses": total_responses,
        "posts": posts,
        "conteo": conteo_por_tipo,
        "chart_data": json.dumps(chart_config),  # Pasamos la configuración del gráfico como JSON
    }

    return render(request, "dashboard/index.html", data)
def chart_data(response):
    responses_by_date = defaultdict(int)
    
    # Contamos las respuestas por fecha
    for post_id, post_data in response.items():
        current_date = None
        if 'fecha' in post_data:
            try:
                current_date = datetime.fromisoformat(post_data['fecha'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass

        if current_date:
            date_key = current_date.strftime('%Y-%m-%d')
            responses_by_date[date_key] += 1
    
    # Ordenamos las fechas
    sorted_dates = sorted(responses_by_date.keys())
    
    labels = []  # Fechas para el eje X
    data_points = []  # Número de respuestas por fecha para el eje Y
    
    # Rellenamos los labels y los data points
    for date_str in sorted_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d/%m/%Y')
        labels.append(formatted_date)
        data_points.append(responses_by_date[date_str])  # Solo el número de respuestas por fecha
    
    # Configuración del gráfico
    chart_config = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Número de personas que votaron',
                'backgroundColor': '#0694a2',
                'borderColor': '#0694a2',
                'data': data_points,  # Datos con el número de respuestas por fecha
                'fill': False,
            }
        ]
    }

    return chart_config
