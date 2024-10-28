import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #gráfica
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score

pd.options.display.float_format = '{:.2f}'.format # Para visualizar 2decimales en los DF

import warnings
warnings.filterwarnings('ignore')

Modalidad = {
    'Estudios': [0, 1, 2, 3, 4],
    'Ocupacion': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    'Horario': [17, 18, 19, 20, 21, 22, 23, 24],
    'Sexo': [25, 26],
    'Edad': [27, 28, 29, 30, 31]
}

perfil_general = pd.read_excel("./data/V3_Analisis_cluster_escalar_datos.xlsx", sheet_name=0)
sitios_cant = pd.read_excel("./data/V3_Analisis_cluster_escalar_datos.xlsx", sheet_name=1)
sitios_porc = pd.read_excel("./data/V3_Analisis_cluster_escalar_datos.xlsx", sheet_name=2)

def get_reeomendacion(cluster, sitios):
    porc = 0.5
    lista_sitios = []
    for col in sitios.columns.to_list():
        if sitios_porc.loc[cluster, col] >= porc:
            lista_sitios.append(col)
    return lista_sitios


def get_cluster_sum(perfil_general, perfil_turista, Modalidad):
    cluster_values = []
    for _, row in perfil_general.iterrows():
        sum_values = 0
        for m in Modalidad:
            for v in Modalidad[m]:
                variable = perfil_general.columns[v]
                if perfil_turista.get(variable, False):
                    sum_values += float(row[v])
        cluster_values.append(sum_values)
    return cluster_values.index(max(cluster_values))

def get_cluster_owa(perfil_general, perfil_turista, Modalidad):
    # owa = np.array([0.1, 0.1, 0.2, 0.2, 0.4])
    owa = np.array([0.0, 0.5, 0.3, 0.2, 0.0])
    df = pd.DataFrame(columns=Modalidad.keys())
    for _, row in perfil_general.iterrows():
        cluster_values = {}
        for m in Modalidad:
            cluster_values[m] = [0]
            for v in Modalidad[m]:
                variable = perfil_general.columns[v]
                if perfil_turista.get(variable, False):
                    cluster_values[m][0] += float(row[v])
        df = pd.concat([df, pd.DataFrame(cluster_values)], ignore_index=True)

    cluster_values = []
    for _, row in df.iterrows():
        values = row.tolist()
        values.sort(reverse=True)
        sum_owa = np.asarray(values) * owa
        cluster_values.append(sum_owa.sum())

    return cluster_values.index(max(cluster_values)), df

# formato de recibimiento del formulario
perfil_turista = {
    'Primaria': True,
    'Secundaria': True,
    'Formacion_Tecnica': False,
    'Universidad': True,
    'Posgrado': True,
    'Actividades_salud_humana': False,
    'Actividades_profesionales_cientificas': True,
    'Administracion_Publica_defensa': False,
    'Actividades_artisticas_entretenimiento': False,
    'Comercio_al_por_mayor': False,
    'Desempleado': False,
    'Ensenanza': False,
    'Actividades_de_alojamiento_y_servicio_de_comida': False,
    'Ocupacion_Estudiante': False,
    'Informacion_comunicaciones': False,
    'Otras_actividades': False,
    'Pensionado': False,
    'Manana': False,
    'Tarde': False,
    'Noche': True,
    'Man/Tar': False,
    'Man/Noc': False,
    'Tar/Noc': True,
    'Indiferente': False,
    'Mujer': True,
    'Hombre': False,
    '1825': False,
    '2635': True,
    '3650': False,
    '5164': False,
    '6585': False
}


cluster, df = get_cluster_owa(perfil_general, perfil_turista, Modalidad)
print('El cluster para el Turista (Formula OWA) es:', cluster)
print('Sitios recomendados para el Turista:', get_reeomendacion(cluster, sitios_porc))

cluster = get_cluster_sum(perfil_general, perfil_turista, Modalidad)
print('El cluster para el Turista (Formula suma) es:', cluster)
print('Sitios recomendados para el Turista:', get_reeomendacion(cluster, sitios_porc))