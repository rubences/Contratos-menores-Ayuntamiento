# Programa de análisis de los contatos menores del Ayuntamiento de Madrid
# Autor: Alfredo Sánchez Alberca (asalber@ceu.es)
from contratos import *

# Carga de datos
ruta = 'datos/datos-contratos-menores.csv'
try:
    df = pd.read_csv(ruta, sep=';')
except FileNotFoundError:
    print('El fichero ', ruta, 'no existe')
else:
    # Preprocesamiento de datos
    # # Ordenar el dataframe por años
    df = df.sort_values(['AÑO'])
    print(df)
    print(facturacion_empresa_años(df, 'B28380582', [2018, 2019]))
    print(gasto_seccion_años(df, 'EMPRESA MUNICIPAL DE TRANSPORTES S.A.', [2018, 2019]))
    print(facturacion_empresa_seccion_años(df, 'B80176936', 'EMPRESA MUNICIPAL DE TRANSPORTES S.A.', [2018, 2019]))
    empresas_mayor_facturacion(df, [2018,2019], n = 10)
    evolucion_empresas_mayor_facturacion(df, 2017, 2019)
    evolucion_facturacion_secciones(df, 2017, 2019)

