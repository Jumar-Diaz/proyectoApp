from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recomendacion
from .serializers import RecomendacionSerializer, CalificacionSerializer, CalificacionImageSerializer
from .newRecomendacion import get_cluster_owa, get_reeomendacion
from .pictures import obtenerClubster
from .description import obtenerClubsterDescription
import pandas as pd

perfil_general = pd.read_excel("./data/V3_Analisis_cluster_escalar_datos.xlsx", sheet_name=0)
sitios_porc = pd.read_excel("./data/V3_Analisis_cluster_escalar_datos.xlsx", sheet_name=2)

Modalidad = {
    'Estudios': [0, 1, 2, 3, 4],
    'Ocupacion': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    'Horario': [17, 18, 19, 20, 21, 22, 23, 24],
    'Sexo': [25, 26],
    'Edad': [27, 28, 29, 30, 31]
}

# Función de recomendación
def recomendacion_turista(perfil_turista):
    cluster, _ = get_cluster_owa(perfil_general, pd.Series(perfil_turista), Modalidad)
    recomendaciones = get_reeomendacion(cluster, sitios_porc)
    return cluster, recomendaciones

@api_view(['POST'])
def save_calification(request):
    if request.method == 'POST':
        # Procesar el formulario enviado desde Angular
        data = request.data
        print("Data ----> ", data);
        serializer = CalificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def save_calification_image(request):
    if request.method == 'POST':
        #procesar calificacion de imagen
        data = request.data
        print("Calificacion Imagen ----> ", data);
        serializer = CalificacionImageSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def recomendacion_view(request):
    if request.method == 'POST':
        # Procesar el formulario enviado desde Angular
        data = request.data
        print("Request: ", data);
        #  name = data.get('name', '')
        perfil_turista = data.get('perfil_turista','');

        print("perfil_turista: ", perfil_turista);
        #  print("Name: ", name);


        print("perfil: ", perfil_turista)


        # print("DATA: ", data.perfil_turista);
        # Crear o actualizar el perfil del turista
        # turista, _ = Turista.objects.get_or_create(name=name)
        # turista_serializer = TuristaSerializer(instance=turista, data={'name': name})
        # if turista_serializer.is_valid():
            # turista_serializer.save()
        # else:
            # return Response(turista_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Realizar la recomendación usando la función recomendacion_turista
        cluster, recomendaciones = recomendacion_turista(perfil_turista)
        images = obtenerClubster(cluster)
        description = obtenerClubsterDescription(cluster)

        # Guardar la recomendación en la base de datos
        recomendacion = Recomendacion.objects.create(cluster=cluster, recomendaciones=recomendaciones, images=images, description=description)
        #recomendacion = Recomendacion.objects.create(turista=turista, cluster=cluster, recomendaciones=recomendaciones, images=images)

        print("cluster:",cluster)
        print("Recomendacion:",recomendaciones)

        # Serializar y devolver los resultados
        recomendacion_serializer = RecomendacionSerializer(recomendacion)
        return Response(recomendacion_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def lista_recomendaciones(request):
    if request.method == 'GET':
        recomendaciones = Recomendacion.objects.all()
        serializer = RecomendacionSerializer(recomendaciones, many=True)
        return Response(serializer.data)

