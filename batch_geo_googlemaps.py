# ----------------------------------------------------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTÉCAS NECESSÁRIAS
# ----------------------------------------------------------------------
import os
import googlemaps
import pandas as pd


# ----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO CLIENTE GOOGLE MAPS
# ----------------------------------------------------------------------

# A chave deve ser definida como uma variável de ambiente (ex: export CHAVE_API_GOOGLE="SUA_CHAVE")
CHAVE_API_GEOCODING_GoogleMaps = os.environ.get("CHAVE_API_GEOCODING_GoogleMaps") 
gmaps = None

try:
    if CHAVE_API_GOOGLE:
        # Tenta iniciar o cliente da API
        gmaps = googlemaps.Client(key=CHAVE_API_GOOGLE)
        print("Cliente Google Maps inicializado com sucesso.")
    else:
        print("AVISO: A variável de ambiente CHAVE_API_GOOGLE não foi definida.")
except Exception as e:
    # Captura e exibe qualquer erro de inicialização
    print(f"ERRO CRÍTICO ao iniciar o cliente Google Maps: {e}")
    gmaps = None


# ----------------------------------------------------------------------
# 3. FUNÇÃO DE GEOCODIFICAÇÃO
# ----------------------------------------------------------------------

def get_coordenadas_google(query):

    """
    Converte um endereço de texto em coordenadas geográficas (Lat/Lon) usando 
    a API do Google Maps.
    
    Args:
        query_completa (str): O endereço ou nome do local a ser geocodificado.
        
    Returns:
        pd.Series: Uma série do Pandas contendo [latitude, longitude].
                   Retorna [None, None] em caso de falha.
    """
    
    # Se o cliente não foi inicializado (gmaps é None), não prossegue
    if gmaps is None: 
        return pd.Series([None, None])
        
    try:
        # Realiza a chamada à API
        geocode_result = gmaps.geocode(query)
        
        if geocode_result:
            # Extrai as coordenadas do primeiro resultado
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
            return pd.Series([lat, lon])
        else:
            # Retorna None se a API não encontrar o endereço
            print(f"AVISO: Endereço não encontrado pela API. Consulta: {query}")
            return pd.Series([None, None]) 
            
    except Exception as e:
        # Trata erros inesperados da API (limite de uso, rede, etc.)
        print(f"ERRO na API: {e} | Consulta: {query}")
        return pd.Series([None, None])

# ----------------------------------------------------------------------
# 4. EXECUÇÃO DA FUNÇÃO
# ----------------------------------------------------------------------

# Considerando que 'df' é um DataFrame carregado com a coluna de texto a ser geocodificada.
df[["latitude", "longitude"]] = df['ENDERECO'].apply(get_coordenadas_google)