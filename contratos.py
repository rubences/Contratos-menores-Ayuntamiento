"""Módulo que contiene funciones para analizar la base de datos de contratos menores del Ayuntamiento de Madrid.
https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=c331ef300ebe5610VgnVCM1000001d4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def empresa(df, nif):
    """
    Función que devuelve el nombre de la empresa con el nif dado.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de los contratos menores.
        - nif: Es una cadena con el NIF del contratista.
    Devuelve:
        El nombre del contratista.
    """
    return df[df['NIF']==nif]['CONTRATISTA'].iloc[0]


def facturacion_empresa_años(df, nif, años):
    """
    Función que devuelve un diccionario con el número de contratos y el total facturado por la empresa durante una lista de años.
    Parámetros: 
        - df: Es un DataFrame con la información de la base de datos de los contratos menores.
        - nif: Es una cadena con el NIF del contratista.
        - años: Es una lista con los años. 
    Devuelve:
        Un diccionario con el número de contratos y el total facturado por la empresa con el nif dado durante los años indicados.
    """
    # Filtro de la empresa y los años
    df1 = df[(df['NIF'] == nif) & (df['AÑO'].isin(años))]
    return {'Número de contratos': df1['IMPORTE'].count(), 'Total facturado':df1['IMPORTE'].sum()}

def gasto_seccion_años(df, seccion, años):
    """
    Función que devuelve un diccionario con el número de contratos y el total gastado por una sección del ayuntamiento durante una lista de años.
    Parámetros: 
        - df: Es un DataFrame con la información de la base de datos de los contratos menores.
        - seccion: Es una cadena con la sección del ayuntamiento que ordena el gasto.
        - años: Es una lista con los años. 
    Devuelve:
        Un diccionario con el número de contratos y el total facturado por la empresa con el nif dado durante los años indicados.
    """
    # Filtro de la sección y los años
    df1 = df[(df['SECCION'] == seccion) & (df['AÑO'].isin(años))]
    return {'Número de contratos': df1['IMPORTE'].count(), 'Total gastado':df1['IMPORTE'].sum()}

def facturacion_empresa_seccion_años(df, nif, seccion, años):
    """
    Función que devuelve un diccionario con el número de contratos y el total facturado por la empresa a una seccion durante una lista de años.
    Parámetros: 
        - df: Es un DataFrame con la información de la base de datos de los contratos menores.
        - nif: Es una cadena con el NIF del contratista.
        - seccion: Es una cadena con la sección del ayuntamiento que ordena el gasto.
        - años: Es una lista con los años. 
    Devuelve:
        Un diccionario con el número de contratos y el total facturado por la empresa con el nif dado a la sección dada durante los años indicados.
    """
    # Filtro de la empresa, la sección y los años
    df1 = df[(df['NIF'] == nif) & (df['SECCION'] == seccion) & (df['AÑO'].isin(años))]
    return {'Número de contratos': df1['IMPORTE'].count(), 'Total facturado':df1['IMPORTE'].sum()}

def empresas_mayor_facturacion(df, años, n = 10):
    """
    Función que imprime una tabla con las n empresas que más han facturado durante los años indicados y genera un gráfico con esa información.
    Parámetros: 
        - df: Es un DataFrame con la información de la base de datos de los contratos menores.
        - años: Es una lista con los años. 
        - n: Es el número de empresas en la tabla (10 por defecto)
    """
    # Filtro de los años
    df1 = df[df['AÑO'].isin(años)]
    # Agrupar por empresas
    df1 = df1.groupby('NIF')['IMPORTE'].sum()
    # Ordenar descendentemente por importe
    df1 = df1.sort_values(ascending=False)
    # Obtener los n primeros y establecer el nombre de la empresa como índice.
    df1 = df1[:n].rename(lambda x: empresa(df, x))
    # Imprimirlos
    print(df1)
    # Inicializamos el gráfico
    fig, ax = plt.subplots(figsize=(6, 8))
    # Dibujar el diagrama de barras
    df1.plot(kind = 'bar', ax = ax)
    # Título del gráfico
    ax.set_title(str(n) + ' empresas con mayor facturación (años ' + str(años) + ')')
    # Título del eje x
    ax.set_ylabel('Importe total en €')
    # Ajustar los márgenes del gráfico
    plt.tight_layout()
    plt.gcf().subplots_adjust(bottom=0.6)
    # Guardamos el gráfico
    plt.savefig('img/empresas-mayor-facturacion-' + str(n) + '.png')
    return

def evolucion_empresas_mayor_facturacion(df, inicio, fin, n = 10):
    """
    Función que crea un gráfico con la evolución anual del total facturado por las n empresas con mayor facturación en un rango de años dado.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - inicio: Es un entero con el año inicial.
        - fin: Es un entero con el año final.
        - n: Es el número de empresas en el gráfico (10 por defecto)
    """
     # Filtro de los años
    df1 = df[(df['AÑO'] >= inicio) & (df['AÑO'] <= fin)]
    # Agrupar por empresas
    df2 = df1.groupby('NIF')['IMPORTE'].sum()
    # Ordenar descendentemente por importe
    df2 = df2.sort_values(ascending = False)
    # Obtener la lista de los nifs de las n empresas con mayor facturación
    nifs = df2[:n].index
    # Filtrar las n empresas con mayor facturación en el rango de años
    df1 = df1[df1['NIF'].isin(list(nifs))]
    # Agrupar por años y empresas
    df1 = df1.groupby(['AÑO', 'NIF'])['IMPORTE'].sum()
    # Establecer como índice el nombre de la empresa
    df1 = df1.rename(lambda x: empresa(df, x), level = 1)
    # Inicializamos el gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    # Desagrupamos por empresas y generamos el gráfico de líneas
    df1.unstack().plot(legend = True, ax = ax)
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Título del gráfico
    ax.set_title('Evolución facturacion ' + str(n) + ' empresas con mayor facturación')
    # Título del eje x
    ax.set_ylabel('Importe anual en €')
    # Establecer las marcas del eje x
    ax.set_xticks(range(inicio, fin+1))
    # Ajustar los márgenes del gráfico
    # plt.tight_layout()
    # Guardamos el gráfico.
    plt.savefig('img/evolucion-empresas-mayor-facturacion' +  str(n) + '.png', bbox_inches='tight')
    return

def evolucion_facturacion_secciones(df, inicio, fin):
    """
    Función que crea un gráfico con la evolución de la facturacion anual por secciones en un rango de años dado.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - inicio: Es un entero con el año inicial.
        - fin: Es un entero con el año final.
    """
     # Filtro de los años
    df1 = df[(df['AÑO'] >= inicio) & (df['AÑO'] <= fin)]
    # Agrupar por años y secciones
    df1 = df1.groupby(['AÑO', 'SECCION'])['IMPORTE'].sum()
    # Inicializamos el gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    # Desagrupamos por secciones y generamos el gráfico de líneas
    df1.unstack().plot(legend = True, ax = ax)
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Título del gráfico
    ax.set_title('Evolución facturacion por secciones')
    # Título del eje x
    ax.set_ylabel('Importe anual en €')
    # Establecer las marcas del eje x
    ax.set_xticks(range(inicio, fin+1))
    # Guardamos el gráfico.
    plt.savefig('img/evolucion-secciones-' + str(inicio) + ':' + str(fin) + '.png', bbox_inches = 'tight')
    return
