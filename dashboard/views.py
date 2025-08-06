from django.shortcuts import render

import requests
from django.conf import settings


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

    data = {
        "title": "Landing Page' Dashboard",
        "total_responses": total_responses,
        "posts": posts,
        "conteo": conteo_por_tipo,
    }

    return render(request, "dashboard/index.html", data)
