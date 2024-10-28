from django.urls import path
from .views import recomendacion_view, lista_recomendaciones, save_calification, save_calification_image

urlpatterns = [
    path('recomendacion/', recomendacion_view, name='recomendacion'),
    path('recomendaciones/', lista_recomendaciones, name='lista_recomendaciones'),
    path('calification/save', save_calification, name="guardarCalificacion"),
    path('calificationImage/saveImage', save_calification_image, name="guardarCalificationImage"),
]
