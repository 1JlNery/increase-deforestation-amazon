import geopandas as gpd
import os
import time
import pickle

def cache_shapefile(shapefile_path, cache_path):
    if os.path.exists(cache_path):
        print("Carregando o cache...")
        with open(cache_path, 'rb') as f:
            gdf = pickle.load(f)
    else:
        print("Inicializando o cache do shapefile...")
        gdf = gpd.read_file(shapefile_path)
        with open(cache_path, 'wb') as f:
            pickle.dump(gdf, f)
    return gdf

tempoInicio = time.time()
shapefile_path = os.environ.get("pathShapefile")
cache_path = os.environ.get("pathCache")

if not os.path.exists(shapefile_path):
    print(f"Arquivo não encontrado: {shapefile_path}")
else:
    gdf = cache_shapefile(shapefile_path, cache_path)

anoProcurado = int(input("digite o ano: "))    

gdf_sorted = gdf.sort_values(by="year", ascending=True)
dates = gdf_sorted["year"].tolist()

def pesquisaBinaria(lista, id):
    baixo = 0
    alto = len(lista) - 1
    primeiroDado = None

    while baixo <= alto:
        meio = (baixo + alto) // 2
        chute = lista[meio]
        if chute == id:
            primeiroDado = meio
            alto = meio - 1
        elif chute > id:
            alto = meio - 1
        else:
            baixo = meio + 1
    return primeiroDado
        
anoEncontrado = pesquisaBinaria(dates, anoProcurado)

if anoEncontrado is not None:
    resultados = []
    i = anoEncontrado
    while i < len(dates) and dates[i] == anoProcurado:
        resultados.append(gdf_sorted.iloc[i])
        i += 1
    resultadoDado = gpd.GeoDataFrame(resultados)
    print("resultado encontrado: \n",resultadoDado)
else:
    print("data não foi encontrada")

tempoFinal = time.time()
tempoTotal = round(tempoFinal - tempoInicio)
print(f"Tempo executando: {tempoTotal}s")